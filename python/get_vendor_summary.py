import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

DB_PATH = Path("../data/inventory.db")
OUTPUT_PATH = Path("../data/vendor_sales_summary_clean.csv")


# ============================================================
# CREATE VENDOR SUMMARY
# ============================================================

def create_vendor_summary(conn):

    query = """
    WITH FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Volume,
            pp.Price AS ActualPrice,

            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars

        FROM purchases p

        LEFT JOIN purchase_prices pp
            ON p.Brand = pp.Brand

        WHERE p.PurchasePrice > 0

        GROUP BY
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Volume,
            pp.Price
    ),

    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,

            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax

        FROM sales

        GROUP BY
            VendorNo,
            Brand
    )

    SELECT

        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,

        ps.PurchasePrice,
        ps.Volume,
        ps.ActualPrice,

        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,

        COALESCE(ss.TotalSalesQuantity, 0)
            AS TotalSalesQuantity,

        COALESCE(ss.TotalSalesDollars, 0)
            AS TotalSalesDollars,

        COALESCE(ss.TotalSalesPrice, 0)
            AS TotalSalesPrice,

        COALESCE(ss.TotalExciseTax, 0)
            AS TotalExciseTax,

        COALESCE(fs.FreightCost, 0)
            AS FreightCost

    FROM PurchaseSummary ps

    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand

    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber

    ORDER BY ps.TotalPurchaseDollars DESC
    """

    print("Creating vendor summary...")

    df = pd.read_sql_query(query, conn)

    print(f"Vendor summary created: {len(df):,} rows")

    return df


# ============================================================
# CLEAN DATA
# ============================================================

def clean_data(df):

    print("Cleaning data...")

    # Numeric conversion
    numeric_columns = [
        "PurchasePrice",
        "Volume",
        "ActualPrice",
        "TotalPurchaseQuantity",
        "TotalPurchaseDollars",
        "TotalSalesQuantity",
        "TotalSalesDollars",
        "TotalSalesPrice",
        "TotalExciseTax",
        "FreightCost"
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Missing values
    df[numeric_columns] = df[numeric_columns].fillna(0)

    # Clean text
    df["VendorName"] = (
        df["VendorName"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    df["Description"] = (
        df["Description"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    # ========================================================
    # DERIVED KPIs
    # ========================================================

    # Gross Profit
    df["GrossProfit"] = (
        df["TotalSalesDollars"]
        - df["TotalPurchaseDollars"]
    )

    # Profit Margin
    df["ProfitMargin"] = np.where(
        df["TotalSalesDollars"] != 0,
        (df["GrossProfit"] /
         df["TotalSalesDollars"]) * 100,
        0
    )

    # Stock Turnover
    df["StockTurnover"] = np.where(
        df["TotalPurchaseQuantity"] != 0,
        df["TotalSalesQuantity"] /
        df["TotalPurchaseQuantity"],
        0
    )

    # Sales-to-Purchase Ratio
    df["SalesToPurchaseRatio"] = np.where(
        df["TotalPurchaseDollars"] != 0,
        df["TotalSalesDollars"] /
        df["TotalPurchaseDollars"],
        0
    )

    return df


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 60)
    print("VENDOR PERFORMANCE ANALYTICS - ETL")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)

    try:

        # Create summary
        vendor_summary = create_vendor_summary(conn)

        print("\nFirst 5 rows:")
        print(
            vendor_summary.head().to_string(index=False)
        )

        # Clean data
        clean_df = clean_data(vendor_summary)

        print("\nCleaned data preview:")
        print(
            clean_df.head().to_string(index=False)
        )

        # Save CSV
        clean_df.to_csv(
            OUTPUT_PATH,
            index=False
        )

        print("\n" + "=" * 60)
        print("ETL COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print(f"\nOutput file:")
        print(OUTPUT_PATH)

        print(f"\nFinal rows: {len(clean_df):,}")
        print(f"Final columns: {len(clean_df.columns)}")

    except Exception as e:

        print("\nERROR:")
        print(e)

    finally:
        conn.close()


if __name__ == "__main__":
    main()