import os
import json
import pandas as pd

from google.cloud import bigquery
from google.oauth2 import service_account

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
    project=credentials_info["banking-etl-project"]
)

# Read transformed file
df = pd.read_csv(
    "data/customer_summary.csv"
)

# BigQuery Table
table_id = "banking-etl-project.banking_data.customer_summary"

# Load Data
job = client.load_table_from_dataframe(
    df,
    table_id
)

job.result()

print("Data Loaded to BigQuery Successfully!")