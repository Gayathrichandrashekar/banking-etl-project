from faker import Faker
import pandas as pd
import random

fake = Faker('en_IN')

# --------------------
# CUSTOMERS
# --------------------

customers = []

for i in range(1, 10001):

    customers.append([
        i,
        fake.name(),
        fake.city()
    ])

customer_df = pd.DataFrame(
    customers,
    columns=[
        "customer_id",
        "name",
        "city"
    ]
)

customer_df.to_csv(
    "data/customers.csv",
    index=False
)

print("customers.csv created")


# --------------------
# ACCOUNTS
# --------------------

accounts = []

for i in range(101, 15101):

    accounts.append([
        i,
        random.randint(1,10000),
        random.choice(
            ["Savings","Current"]
        ),
        random.randint(
            5000,
            500000
        )
    ])

account_df = pd.DataFrame(
    accounts,
    columns=[
        "account_id",
        "customer_id",
        "account_type",
        "balance"
    ]
)

account_df.to_csv(
    "data/accounts.csv",
    index=False
)

print("accounts.csv created")


# --------------------
# TRANSACTIONS
# --------------------

transactions = []

for i in range(1001,51001):

    transactions.append([
        i,
        random.randint(
            101,
            15100
        ),
        random.choice(
            ["Credit","Debit"]
        ),
        random.randint(
            100,
            50000
        )
    ])

txn_df = pd.DataFrame(
    transactions,
    columns=[
        "txn_id",
        "account_id",
        "txn_type",
        "amount"
    ]
)

txn_df.to_csv(
    "data/transactions.csv",
    index=False
)

print("transactions.csv created")
print(len(customer_df))
print(len(account_df))
print(len(txn_df))