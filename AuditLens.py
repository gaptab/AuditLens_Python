import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import Cursor

# Set random seed for reproducibility
np.random.seed(42)

# Create dummy data for 100+ audits (1000 rows)
audit_data = pd.DataFrame({
    "AuditID": range(1, 1001),
    "BusinessSegment": np.random.choice(['Retail', 'Corporate', 'Wealth Management', 'Investment Banking'], size=1000),
    "AuditDate": pd.date_range(start="2023-01-01", periods=1000, freq='h'),
    "Product": np.random.choice(['Loan', 'Investment', 'Insurance', 'Mortgage'], size=1000),
    "RiskScore": np.random.uniform(0, 100, size=1000),  # Risk score between 0-100
    "OperatingEffectiveness": np.random.uniform(50, 100, size=1000),  # Operating Effectiveness score
    "AuditResult": np.random.choice(['Pass', 'Fail'], size=1000, p=[0.75, 0.25]),  # Audit result
})

# Display first few rows
print(audit_data.head())

# Calculate KPIs for product-wise trends
product_kpis = audit_data.groupby('Product').agg(
    TotalAudits=("AuditID", "count"),
    FailedAudits=("AuditResult", lambda x: (x == 'Fail').sum()),
    AvgRiskScore=("RiskScore", "mean"),
    AvgOperatingEffectiveness=("OperatingEffectiveness", "mean")
).reset_index()

# Save the KPI report to a CSV file
product_kpis.to_csv("Product_KPIs_Report.csv", index=False)

# Display KPI report
print(product_kpis)

# Create a risk aggregation model to assign risk ratings based on operating effectiveness
def risk_rating(row):
    if row['OperatingEffectiveness'] < 60:
        return 'High Risk'
    elif 60 <= row['OperatingEffectiveness'] < 80:
        return 'Medium Risk'
    else:
        return 'Low Risk'

# Apply the risk rating to the data
audit_data['RiskRating'] = audit_data.apply(risk_rating, axis=1)

# Generate aggregated risk data for different business segments
risk_aggregation = audit_data.groupby('BusinessSegment').agg(
    HighRiskCount=("RiskRating", lambda x: (x == 'High Risk').sum()),
    MediumRiskCount=("RiskRating", lambda x: (x == 'Medium Risk').sum()),
    LowRiskCount=("RiskRating", lambda x: (x == 'Low Risk').sum()),
    AvgOperatingEffectiveness=("OperatingEffectiveness", "mean")
).reset_index()

# Display risk aggregation for business segments
print(risk_aggregation)

# Visualize the KPIs for product-wise trends
fig, ax = plt.subplots(2, 2, figsize=(15, 12))

# KPI 1: Total Audits by Product
sns.barplot(x="Product", y="TotalAudits", data=product_kpis, ax=ax[0, 0], palette="Set2")
ax[0, 0].set_title("Total Audits by Product")
ax[0, 0].set_xlabel("Product")
ax[0, 0].set_ylabel("Total Audits")

# KPI 2: Failed Audits by Product
sns.barplot(x="Product", y="FailedAudits", data=product_kpis, ax=ax[0, 1], palette="Set1")
ax[0, 1].set_title("Failed Audits by Product")
ax[0, 1].set_xlabel("Product")
ax[0, 1].set_ylabel("Failed Audits")

# KPI 3: Average Risk Score by Product
sns.barplot(x="Product", y="AvgRiskScore", data=product_kpis, ax=ax[1, 0], palette="Blues")
ax[1, 0].set_title("Average Risk Score by Product")
ax[1, 0].set_xlabel("Product")
ax[1, 0].set_ylabel("Average Risk Score")

# KPI 4: Average Operating Effectiveness by Product
sns.barplot(x="Product", y="AvgOperatingEffectiveness", data=product_kpis, ax=ax[1, 1], palette="YlGn")
ax[1, 1].set_title("Average Operating Effectiveness by Product")
ax[1, 1].set_xlabel("Product")
ax[1, 1].set_ylabel("Average Operating Effectiveness")

plt.tight_layout()

# Visualize the Risk Aggregation for Business Segments
fig, ax = plt.subplots(figsize=(10, 6))

# Create a stacked bar plot for risk count by business segment
risk_aggregation.set_index('BusinessSegment')[['HighRiskCount', 'MediumRiskCount', 'LowRiskCount']].plot(
    kind='bar', stacked=True, ax=ax, color=['red', 'orange', 'green'])

ax.set_title("Risk Aggregation by Business Segment")
ax.set_xlabel("Business Segment")
ax.set_ylabel("Risk Count")
ax.legend(title="Risk Rating", labels=["High Risk", "Medium Risk", "Low Risk"])
plt.tight_layout()

# Show visualizations
plt.show()
# Save the audit data to a CSV file
audit_data.to_csv("audit_data.csv", index=False)

# Save the KPI report for products to a CSV file
product_kpis.to_csv("Product_KPIs_Report.csv", index=False)

# Save the risk aggregation report for business segments to a CSV file
risk_aggregation.to_csv("Risk_Aggregation_Report.csv", index=False)

# Print confirmation messages
print("All DataFrames have been saved to CSV files.")
