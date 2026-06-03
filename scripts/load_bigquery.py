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

# Read transformed file
df = pd.read_csv(
    "customer_summary.csv"
)

# BigQuery Table
table_id = "banking-etl-project.banking_data.customer_summary"

# Delete existing table to avoid schema mismatch
client.delete_table(
    table_id,
    not_found_ok=True
)

# Load DataFrame into BigQuery
job = client.load_table_from_dataframe(
    df,
    table_id
)

# Wait for job completion
job.result()

print("Data Loaded to BigQuery Successfully!")