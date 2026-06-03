from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os
import json

# Read credentials from GitHub Secret
credentials_info = json.loads(
    os.environ["GCP_CREDENTIALS"]
)

# Create credentials object
credentials = service_account.Credentials.from_service_account_info(
    credentials_info
)

# Create BigQuery client
client = bigquery.Client(
    credentials=credentials,
    project=credentials_info["project_id"]
)

# ==========================
# Customer Summary
# ==========================

customer_summary = pd.read_csv(
    "customer_summary.csv"
)

table_id = "banking-etl-project.banking_data.customer_summary"

client.delete_table(
    table_id,
    not_found_ok=True
)

job = client.load_table_from_dataframe(
    customer_summary,
    table_id
)

job.result()

print("customer_summary loaded")

# ==========================
# High Value Customers
# ==========================

high_value_customers = pd.read_csv(
    "high_value_customers.csv"
)

table_id = "banking-etl-project.banking_data.high_value_customers"

client.delete_table(
    table_id,
    not_found_ok=True
)

job = client.load_table_from_dataframe(
    high_value_customers,
    table_id
)

job.result()

print("high_value_customers loaded")

# ==========================
# Transactions Transformed
# ==========================

transactions = pd.read_csv(
    "transactions_transformed.csv"
)

table_id = "banking-etl-project.banking_data.transactions_transformed"

client.delete_table(
    table_id,
    not_found_ok=True
)

job = client.load_table_from_dataframe(
    transactions,
    table_id
)

job.result()

print("transactions_transformed loaded")

print("All tables loaded successfully!")