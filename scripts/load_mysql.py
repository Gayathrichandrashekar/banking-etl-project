import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

engine = create_engine(
    "mysql+mysqlconnector://root:root@mysql:3306/banking",
    connect_args={
        "host": "mysql",
        "port": 3306
    }
)

customers = pd.read_csv("data/customers.csv")
accounts = pd.read_csv("data/accounts.csv")
transactions = pd.read_csv("data/transactions.csv")

customers.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False
)

accounts.to_sql(
    "accounts",
    engine,
    if_exists="append",
    index=False
)

transactions.to_sql(
    "transactions_tbl",
    engine,
    if_exists="append",
    index=False
)

print("Customers Loaded:", len(customers))
print("Accounts Loaded:", len(accounts))
print("Transactions Loaded:", len(transactions))
print("Data Loaded Successfully!")