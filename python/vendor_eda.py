import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = Path("../data/vendor_sales_summary_clean.csv")
OUTPUT_DIR = Path("../screenshots/eda")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("VENDOR PERFORMANCE ANALYTICS - EDA")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

# ============================================================
# 1. DATASET INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

# ============================================================
# 2. MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

missing = df.isnull().sum()

print(missing[missing > 0])

# ============================================================
# 3. DUPLICATES
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE ANALYSIS")
print("=" * 60)

duplicates = df.duplicated().sum()

print(f"Duplicate rows: {duplicates:,}")

# ============================================================
# 4. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

numeric_columns = df.select_dtypes(
    include=np.number
).columns

print(
    df[numeric_columns].describe().round(2)
)

# ============================================================
# 5. TOP 10 VENDORS BY SALES
# ============================================================

vendor_sales = (
    df.groupby(["VendorNumber", "VendorName"])
    ["TotalSalesDollars"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 VENDORS BY SALES")
print("=" * 60)

print(vendor_sales)

plt.figure(figsize=(12, 6))

vendor_sales.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Vendors by Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Vendor")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_vendors_sales.png",
    dpi=300
)

plt.close()

# ============================================================
# 6. TOP 10 VENDORS BY GROSS PROFIT
# ============================================================

vendor_profit = (
    df.groupby(["VendorNumber", "VendorName"])
    ["GrossProfit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 VENDORS BY GROSS PROFIT")
print("=" * 60)

print(vendor_profit)

plt.figure(figsize=(12, 6))

vendor_profit.sort_values().plot(
    kind="barh"
)

plt.title("Top 10 Vendors by Gross Profit")
plt.xlabel("Gross Profit ($)")
plt.ylabel("Vendor")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "top_vendors_profit.png",
    dpi=300
)

plt.close()

# ============================================================
# 7. PROFIT MARGIN DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

sns.histplot(
    df["ProfitMargin"],
    bins=50,
    kde=True
)

plt.title("Distribution of Vendor Profit Margins")
plt.xlabel("Profit Margin (%)")
plt.ylabel("Number of Records")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "profit_margin_distribution.png",
    dpi=300
)

plt.close()

# ============================================================
# 8. SALES VS PURCHASES
# ============================================================

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=df,
    x="TotalPurchaseDollars",
    y="TotalSalesDollars",
    alpha=0.5
)

plt.title("Sales vs Purchase Dollars")
plt.xlabel("Total Purchase Dollars")
plt.ylabel("Total Sales Dollars")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "sales_vs_purchases.png",
    dpi=300
)

plt.close()

# ============================================================
# 9. STOCK TURNOVER
# ============================================================

stock_turnover = (
    df.groupby(["VendorNumber", "VendorName"])
    ["StockTurnover"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 VENDORS BY STOCK TURNOVER")
print("=" * 60)

print(stock_turnover)

# ============================================================
# 10. SALES-TO-PURCHASE RATIO
# ============================================================

ratio = (
    df.groupby(["VendorNumber", "VendorName"])
    ["SalesToPurchaseRatio"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 VENDORS BY SALES-TO-PURCHASE RATIO")
print("=" * 60)

print(ratio)

# ============================================================
# 11. TOP BRANDS BY SALES
# ============================================================

brand_sales = (
    df.groupby(["Brand", "Description"])
    ["TotalSalesDollars"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n" + "=" * 60)
print("TOP 10 BRANDS BY SALES")
print("=" * 60)

print(brand_sales)

# ============================================================
# 12. CORRELATION ANALYSIS
# ============================================================

correlation_columns = [
    "TotalPurchaseDollars",
    "TotalSalesDollars",
    "GrossProfit",
    "ProfitMargin",
    "StockTurnover",
    "SalesToPurchaseRatio",
    "FreightCost",
    "TotalExciseTax"
]

correlation = df[
    correlation_columns
].corr()

print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

print(correlation.round(2))

plt.figure(figsize=(10, 8))

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f"
)

plt.title("Vendor Performance Correlation Matrix")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "correlation_matrix.png",
    dpi=300
)

plt.close()

# ============================================================
# 13. OVERALL KPIs
# ============================================================

total_purchase = df["TotalPurchaseDollars"].sum()
total_sales = df["TotalSalesDollars"].sum()
total_profit = df["GrossProfit"].sum()

overall_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

print("\n" + "=" * 60)
print("OVERALL BUSINESS KPIs")
print("=" * 60)

print(f"Total Purchase: ${total_purchase:,.2f}")
print(f"Total Sales: ${total_sales:,.2f}")
print(f"Gross Profit: ${total_profit:,.2f}")
print(f"Profit Margin: {overall_margin:.2f}%")

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nCharts saved to:")
print(OUTPUT_DIR)