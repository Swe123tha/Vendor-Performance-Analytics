-- ============================================================
-- VENDOR PERFORMANCE ANALYTICS
-- SQL ANALYSIS
-- ============================================================


-- ============================================================
-- 1. DATABASE OVERVIEW
-- ============================================================

SELECT name AS table_name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;


-- ============================================================
-- 2. ROW COUNTS
-- ============================================================

SELECT 'begin_inventory' AS table_name, COUNT(*) AS row_count
FROM begin_inventory

UNION ALL

SELECT 'end_inventory', COUNT(*)
FROM end_inventory

UNION ALL

SELECT 'purchase_prices', COUNT(*)
FROM purchase_prices

UNION ALL

SELECT 'purchases', COUNT(*)
FROM purchases

UNION ALL

SELECT 'sales', COUNT(*)
FROM sales

UNION ALL

SELECT 'vendor_invoice', COUNT(*)
FROM vendor_invoice

UNION ALL

SELECT 'vendor_sales_summary', COUNT(*)
FROM vendor_sales_summary;


-- ============================================================
-- 3. TOP VENDORS BY TOTAL PURCHASE DOLLARS
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    SUM(TotalPurchaseDollars) AS TotalPurchaseDollars
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
ORDER BY TotalPurchaseDollars DESC
LIMIT 10;


-- ============================================================
-- 4. TOP VENDORS BY TOTAL SALES DOLLARS
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    SUM(TotalSalesDollars) AS TotalSalesDollars
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
ORDER BY TotalSalesDollars DESC
LIMIT 10;


-- ============================================================
-- 5. TOP VENDORS BY GROSS PROFIT
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    SUM(GrossProfit) AS GrossProfit
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
ORDER BY GrossProfit DESC
LIMIT 10;


-- ============================================================
-- 6. TOP VENDORS BY PROFIT MARGIN
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    SUM(GrossProfit) AS GrossProfit,
    SUM(TotalSalesDollars) AS TotalSalesDollars,
    ROUND(
        SUM(GrossProfit) * 100.0 /
        NULLIF(SUM(TotalSalesDollars), 0),
        2
    ) AS ProfitMarginPercentage
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
HAVING SUM(TotalSalesDollars) > 0
ORDER BY ProfitMarginPercentage DESC
LIMIT 10;


-- ============================================================
-- 7. VENDOR PURCHASE CONTRIBUTION
-- ============================================================

WITH vendor_purchase AS (
    SELECT
        VendorNumber,
        VendorName,
        SUM(TotalPurchaseDollars) AS PurchaseDollars
    FROM vendor_sales_summary
    GROUP BY VendorNumber, VendorName
),
total_purchase AS (
    SELECT SUM(PurchaseDollars) AS TotalPurchase
    FROM vendor_purchase
)
SELECT
    vp.VendorNumber,
    vp.VendorName,
    ROUND(vp.PurchaseDollars, 2) AS PurchaseDollars,
    ROUND(
        vp.PurchaseDollars * 100.0 /
        NULLIF(tp.TotalPurchase, 0),
        2
    ) AS PurchaseContributionPercentage
FROM vendor_purchase vp
CROSS JOIN total_purchase tp
ORDER BY PurchaseContributionPercentage DESC
LIMIT 20;


-- ============================================================
-- 8. VENDOR SALES CONTRIBUTION
-- ============================================================

WITH vendor_sales AS (
    SELECT
        VendorNumber,
        VendorName,
        SUM(TotalSalesDollars) AS SalesDollars
    FROM vendor_sales_summary
    GROUP BY VendorNumber, VendorName
),
total_sales AS (
    SELECT SUM(SalesDollars) AS TotalSales
    FROM vendor_sales
)
SELECT
    vs.VendorNumber,
    vs.VendorName,
    ROUND(vs.SalesDollars, 2) AS SalesDollars,
    ROUND(
        vs.SalesDollars * 100.0 /
        NULLIF(ts.TotalSales, 0),
        2
    ) AS SalesContributionPercentage
FROM vendor_sales vs
CROSS JOIN total_sales ts
ORDER BY SalesContributionPercentage DESC
LIMIT 20;


-- ============================================================
-- 9. TOP BRANDS BY SALES
-- ============================================================

SELECT
    Brand,
    Description,
    SUM(TotalSalesDollars) AS TotalSalesDollars
FROM vendor_sales_summary
GROUP BY Brand, Description
ORDER BY TotalSalesDollars DESC
LIMIT 20;


-- ============================================================
-- 10. TOP BRANDS BY GROSS PROFIT
-- ============================================================

SELECT
    Brand,
    Description,
    SUM(GrossProfit) AS GrossProfit
FROM vendor_sales_summary
GROUP BY Brand, Description
ORDER BY GrossProfit DESC
LIMIT 20;


-- ============================================================
-- 11. LOW-PERFORMING VENDORS
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    SUM(TotalSalesDollars) AS TotalSalesDollars,
    SUM(GrossProfit) AS GrossProfit,
    ROUND(
        SUM(GrossProfit) * 100.0 /
        NULLIF(SUM(TotalSalesDollars), 0),
        2
    ) AS ProfitMarginPercentage
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
HAVING SUM(TotalSalesDollars) > 0
ORDER BY GrossProfit ASC
LIMIT 20;


-- ============================================================
-- 12. STOCK TURNOVER
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    ROUND(AVG(StockTurnover), 2) AS AverageStockTurnover
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
ORDER BY AverageStockTurnover DESC
LIMIT 20;


-- ============================================================
-- 13. SALES TO PURCHASE RATIO
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    ROUND(AVG(SalesToPurchaseRatio), 2) AS AverageSalesToPurchaseRatio
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
ORDER BY AverageSalesToPurchaseRatio DESC
LIMIT 20;


-- ============================================================
-- 14. FREIGHT COST ANALYSIS
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    ROUND(SUM(FreightCost), 2) AS TotalFreightCost
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
ORDER BY TotalFreightCost DESC
LIMIT 20;


-- ============================================================
-- 15. EXCISE TAX ANALYSIS
-- ============================================================

SELECT
    VendorNumber,
    VendorName,
    ROUND(SUM(TotalExciseTax), 2) AS TotalExciseTax
FROM vendor_sales_summary
GROUP BY VendorNumber, VendorName
ORDER BY TotalExciseTax DESC
LIMIT 20;


-- ============================================================
-- 16. OVERALL BUSINESS KPIs
-- ============================================================

SELECT
    ROUND(SUM(TotalPurchaseDollars), 2) AS TotalPurchases,
    ROUND(SUM(TotalSalesDollars), 2) AS TotalSales,
    ROUND(SUM(GrossProfit), 2) AS TotalGrossProfit,
    ROUND(
        SUM(GrossProfit) * 100.0 /
        NULLIF(SUM(TotalSalesDollars), 0),
        2
    ) AS OverallProfitMargin,
    ROUND(SUM(FreightCost), 2) AS TotalFreightCost,
    ROUND(SUM(TotalExciseTax), 2) AS TotalExciseTax
FROM vendor_sales_summary;