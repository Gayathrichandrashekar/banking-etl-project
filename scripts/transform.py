import pandas as pd

customers = pd.read_csv("data/customers.csv")
accounts = pd.read_csv("data/accounts.csv")
transactions = pd.read_csv("data/transactions.csv")

# Customer balance summary
summary = customers.merge(
    accounts,
    on="customer_id",
    how="inner"
)

customer_summary = (
    summary.groupby(
        ["customer_id", "name"]
    )["balance"]
    .sum()
    .reset_index()
)

customer_summary.rename(
    columns={"balance": "total_balance"},
    inplace=True
)

# High value customers
high_value_customers = customer_summary[
    customer_summary["total_balance"] > 50000
]

# Transaction category
transactions["txn_category"] = transactions["amount"].apply(
    lambda x: "HIGH_VALUE" if x > 10000 else "NORMAL"
)

customer_summary.to_csv(
    "customer_summary.csv",
    index=False
)

high_value_customers.to_csv(
    "high_value_customers.csv",
    index=False
)

transactions.to_csv(
    "transactions_transformed.csv",
    index=False
)

print("Transformation completed")