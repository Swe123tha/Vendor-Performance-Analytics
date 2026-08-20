import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind, sem, t

from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATA_PATH = Path("../data/vendor_sales_summary_clean.csv")
OUTPUT_DIR = Path("../screenshots/statistics")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 65)
print("VENDOR PERFORMANCE - HYPOTHESIS TESTING")
print("=" * 65)

df = pd.read_csv(DATA_PATH)

print(f"\nDataset rows: {len(df):,}")


# ============================================================
# 1. DEFINE TOP AND LOW PERFORMERS
# ============================================================

top_threshold = df["TotalSalesDollars"].quantile(0.75)
low_threshold = df["TotalSalesDollars"].quantile(0.25)

print("\nSales thresholds:")
print(f"Top 25% threshold: ${top_threshold:,.2f}")
print(f"Bottom 25% threshold: ${low_threshold:,.2f}")


top_vendors = df[
    df["TotalSalesDollars"] >= top_threshold
]["ProfitMargin"].dropna()

low_vendors = df[
    df["TotalSalesDollars"] <= low_threshold
]["ProfitMargin"].dropna()


print("\nVendor groups:")
print(f"Top-performing records: {len(top_vendors):,}")
print(f"Low-performing records: {len(low_vendors):,}")


# ============================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 65)
print("PROFIT MARGIN STATISTICS")
print("=" * 65)

print(
    f"\nTop-performing vendors:"
    f"\nMean: {top_vendors.mean():.2f}%"
    f"\nStd: {top_vendors.std():.2f}%"
)

print(
    f"\nLow-performing vendors:"
    f"\nMean: {low_vendors.mean():.2f}%"
    f"\nStd: {low_vendors.std():.2f}%"
)


# ============================================================
# 3. HYPOTHESIS TEST
# ============================================================

print("\n" + "=" * 65)
print("HYPOTHESIS TEST")
print("=" * 65)

print("\nH0: There is no significant difference in mean")
print("    ProfitMargin between top and low-performing vendors.")

print("\nH1: There is a significant difference in mean")
print("    ProfitMargin between top and low-performing vendors.")


# Welch's independent two-sample t-test
t_stat, p_value = ttest_ind(
    top_vendors,
    low_vendors,
    equal_var=False
)

print(f"\nT-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.10f}")


alpha = 0.05

print(f"\nSignificance level: {alpha}")

if p_value < alpha:
    print("\nRESULT:")
    print("Reject H0.")
    print(
        "There is a statistically significant difference "
        "in profit margins between the two groups."
    )
else:
    print("\nRESULT:")
    print("Fail to reject H0.")
    print(
        "There is not enough statistical evidence "
        "to conclude that the profit margins differ."
    )


# ============================================================
# 4. CONFIDENCE INTERVAL FUNCTION
# ============================================================

def calculate_confidence_interval(data, confidence=0.95):

    data = data.dropna()

    mean = data.mean()
    standard_error = sem(data)

    degrees_of_freedom = len(data) - 1

    critical_value = t.ppf(
        (1 + confidence) / 2,
        degrees_of_freedom
    )

    margin_of_error = (
        critical_value * standard_error
    )

    lower = mean - margin_of_error
    upper = mean + margin_of_error

    return mean, lower, upper


# ============================================================
# 5. CALCULATE CONFIDENCE INTERVALS
# ============================================================

top_mean, top_lower, top_upper = (
    calculate_confidence_interval(top_vendors)
)

low_mean, low_lower, low_upper = (
    calculate_confidence_interval(low_vendors)
)


print("\n" + "=" * 65)
print("95% CONFIDENCE INTERVALS")
print("=" * 65)

print(
    f"\nTop-performing vendors:"
    f"\nMean Profit Margin: {top_mean:.2f}%"
    f"\n95% CI: ({top_lower:.2f}%, {top_upper:.2f}%)"
)

print(
    f"\nLow-performing vendors:"
    f"\nMean Profit Margin: {low_mean:.2f}%"
    f"\n95% CI: ({low_lower:.2f}%, {low_upper:.2f}%)"
)


# ============================================================
# 6. VISUALIZE CONFIDENCE INTERVALS
# ============================================================

groups = [
    "Top-performing",
    "Low-performing"
]

means = [
    top_mean,
    low_mean
]

lower_errors = [
    top_mean - top_lower,
    low_mean - low_lower
]

upper_errors = [
    top_upper - top_mean,
    low_upper - low_mean
]


plt.figure(figsize=(10, 6))

plt.errorbar(
    groups,
    means,
    yerr=[
        lower_errors,
        upper_errors
    ],
    fmt="o",
    capsize=8,
    markersize=8
)

plt.ylabel("Mean Profit Margin (%)")
plt.title(
    "95% Confidence Intervals for Vendor Profit Margins"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "profit_margin_confidence_intervals.png",
    dpi=300
)

plt.close()


# ============================================================
# 7. PROFIT MARGIN DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    top_vendors,
    bins=40,
    alpha=0.6,
    label="Top-performing"
)

plt.hist(
    low_vendors,
    bins=40,
    alpha=0.6,
    label="Low-performing"
)

plt.xlabel("Profit Margin (%)")
plt.ylabel("Frequency")

plt.title(
    "Profit Margin Distribution: Top vs Low Performing Vendors"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "profit_margin_group_distribution.png",
    dpi=300
)

plt.close()


# ============================================================
# 8. SAVE STATISTICAL RESULTS
# ============================================================

results = pd.DataFrame({
    "Group": [
        "Top-performing vendors",
        "Low-performing vendors"
    ],
    "MeanProfitMargin": [
        top_mean,
        low_mean
    ],
    "CI_Lower": [
        top_lower,
        low_lower
    ],
    "CI_Upper": [
        top_upper,
        low_upper
    ]
})

results.to_csv(
    OUTPUT_DIR / "confidence_interval_results.csv",
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("STATISTICAL ANALYSIS COMPLETED")
print("=" * 65)

print("\nFiles saved to:")
print(OUTPUT_DIR)
