import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# ---------------------------
# MySQL Connection
# ---------------------------

username = "root"
password = "Deeshna@2025"

engine = create_engine(
    f"mysql+mysqlconnector://{username}:{quote_plus(password)}@localhost/banking"
)

# ---------------------------
# Read Data From MySQL
# ---------------------------

customers = pd.read_sql(
    "SELECT * FROM customers",
    engine
)

accounts = pd.read_sql(
    "SELECT * FROM accounts",
    engine
)

transactions = pd.read_sql(
    "SELECT * FROM transactions_tbl",
    engine
)

print("Data Extracted Successfully")

# ---------------------------
# Data Quality Checks
# ---------------------------

customers = customers.drop_duplicates(
    subset=["customer_id"]
)

customers["city"] = customers["city"].fillna(
    "Unknown"
)

print("Data Quality Checks Completed")

# ---------------------------
# Standardize Data
# ---------------------------

customers["city"] = customers["city"].str.upper()

print("Standardization Completed")

# ---------------------------
# Join Customers + Accounts
# ---------------------------

customer_account = pd.merge(
    customers,
    accounts,
    on="customer_id",
    how="inner"
)

print("Customer Account Join Completed")

# ---------------------------
# Balance Category
# ---------------------------

customer_account["balance_category"] = customer_account[
    "balance"
].apply(
    lambda x:
        "HIGH" if x > 300000
        else "MEDIUM" if x > 100000
        else "LOW"
)

# ---------------------------
# Interest Calculation
# Savings = 4%
# Current = 1%
# ---------------------------

customer_account["interest_earned"] = customer_account.apply(
    lambda row:
        row["balance"] * 0.04
        if row["account_type"] == "Savings"
        else row["balance"] * 0.01,
    axis=1
)

print("Interest Calculation Completed")

# ---------------------------
# Customer Summary
# ---------------------------

customer_summary = customer_account.groupby(
    ["customer_id", "name"]
).agg(
    total_balance=("balance", "sum"),
    total_interest=("interest_earned", "sum"),
    account_count=("account_id", "count")
).reset_index()

print("Customer Summary Created")

# ---------------------------
# High Value Customers
# ---------------------------

high_value_customers = customer_summary[
    customer_summary["total_balance"] > 500000
]

print("High Value Customers Identified")

# ---------------------------
# Transaction Summary
# ---------------------------

transaction_summary = transactions.groupby(
    "account_id"
).agg(
    total_transaction_amount=("amount", "sum"),
    txn_count=("txn_id", "count")
).reset_index()

print("Transaction Summary Created")

# ---------------------------
# VIP Customer Flag
# ---------------------------

customer_summary["risk_flag"] = customer_summary[
    "total_balance"
].apply(
    lambda x:
        "VIP" if x > 1000000
        else "NORMAL"
)

print("Customer Segmentation Completed")

# ---------------------------
# Save Files
# ---------------------------

customer_summary.to_csv(
    "data/customer_summary.csv",
    index=False
)

high_value_customers.to_csv(
    "data/high_value_customers.csv",
    index=False
)

transaction_summary.to_csv(
    "data/transaction_summary.csv",
    index=False
)

print("CSV Files Created Successfully")

# ---------------------------
# Load Results Back To MySQL
# ---------------------------

customer_summary.to_sql(
    "customer_summary",
    engine,
    if_exists="replace",
    index=False
)

high_value_customers.to_sql(
    "high_value_customers",
    engine,
    if_exists="replace",
    index=False
)

transaction_summary.to_sql(
    "transaction_summary",
    engine,
    if_exists="replace",
    index=False
)

print("Transformation Completed Successfully")

print("\nSample Customer Summary")
print(customer_summary.head())