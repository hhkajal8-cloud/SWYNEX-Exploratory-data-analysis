"""
SWYNEX Technologies - Task 2: Exploratory Data Analysis
Dataset: cleaned_data.csv (output of Task 1)
Run:  pip install pandas matplotlib seaborn
      python eda_analysis.py
Charts are saved in the charts/ folder; key numbers print in the console.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
os.makedirs("charts", exist_ok=True)


def save(name):
    plt.tight_layout()
    plt.savefig(f"charts/{name}.png", dpi=150)
    plt.close()


# ---------- 1. Load & overview ----------
df = pd.read_csv("cleaned_data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
df["month"] = df["transaction_date"].dt.to_period("M").dt.to_timestamp()
df["weekday"] = df["transaction_date"].dt.day_name()

print("Shape:", df.shape)
df.info()
print("\nMissing values:\n", df.isnull().sum())
print("\nSummary statistics:\n", df.describe().T)

# ---------- 2. Key statistics ----------
total_rev = df["total_spent"].sum()
print(f"\nTotal revenue: {total_rev:,.2f}")
print(f"Average transaction: {df['total_spent'].mean():.2f}")
print(f"Median transaction: {df['total_spent'].median():.2f}")

# ---------- 3. Charts + insight numbers ----------
# Chart 1: revenue by category
cat = df.groupby("category")["total_spent"].sum().sort_values(ascending=False)
cat.plot(kind="bar", color="steelblue")
plt.title("Total Revenue by Category")
plt.ylabel("Revenue")
save("1_revenue_by_category")
print("\nRevenue share by category (%):\n", (cat / total_rev * 100).round(1))

# Chart 2: monthly revenue trend
monthly = df.groupby("month")["total_spent"].sum()
monthly.plot(marker="o", color="darkorange")
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue")
save("2_monthly_revenue_trend")
print("\nBest month:", monthly.idxmax().strftime("%b %Y"), "->", round(monthly.max(), 2))
print("Weakest month:", monthly.idxmin().strftime("%b %Y"), "->", round(monthly.min(), 2))

# Chart 3: payment method
pay = df.groupby("payment_method")["total_spent"].agg(["count", "sum"])
pay["count"].plot(kind="bar", color="seagreen")
plt.title("Transactions by Payment Method")
plt.ylabel("Number of transactions")
save("3_payment_method")
print("\nPayment method:\n", pay)

# Chart 4: location (online vs in-store)
loc = df.groupby("location")["total_spent"].agg(["count", "sum", "mean"])
loc["sum"].plot(kind="bar", color="mediumpurple")
plt.title("Revenue by Location")
plt.ylabel("Revenue")
save("4_revenue_by_location")
print("\nLocation:\n", loc)

# Chart 5: discount vs no discount
disc = df.groupby("discount_applied")["total_spent"].mean()
disc.plot(kind="bar", color="indianred")
plt.title("Average Spend: Discount vs No Discount")
plt.ylabel("Average Total Spent")
save("5_discount_effect")
print("\nAvg spend by discount:\n", disc)

# Chart 6: top 10 items by revenue
items = df.groupby("item")["total_spent"].sum().sort_values(ascending=False).head(10)
items.sort_values().plot(kind="barh", color="teal")
plt.title("Top 10 Items by Revenue")
plt.xlabel("Revenue")
save("6_top_items")

# Chart 7: sales by weekday
order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
wd = df.groupby("weekday")["total_spent"].sum().reindex(order)
wd.plot(kind="bar", color="goldenrod")
plt.title("Revenue by Day of Week")
plt.ylabel("Revenue")
save("7_revenue_by_weekday")

# Chart 8: distribution of transaction value
sns.histplot(df["total_spent"], bins=30, kde=True, color="slateblue")
plt.title("Distribution of Total Spent")
save("8_total_spent_distribution")

# Chart 9: outliers (boxplot + IQR rule)
sns.boxplot(x=df["total_spent"], color="lightcoral")
plt.title("Outlier Check: Total Spent")
save("9_outliers_boxplot")
q1, q3 = df["total_spent"].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = df[(df["total_spent"] < q1 - 1.5 * iqr) | (df["total_spent"] > q3 + 1.5 * iqr)]
print(f"\nOutliers (IQR rule): {len(outliers)} rows ({len(outliers) / len(df) * 100:.1f}%)")

# Chart 10: correlation heatmap
sns.heatmap(df.select_dtypes("number").corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
save("10_correlation_heatmap")

print("\nDone! Check the charts/ folder.")
