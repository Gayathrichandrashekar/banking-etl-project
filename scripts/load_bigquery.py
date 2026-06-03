from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import os
import json

credentials_info = json.loads(
    os.environ["GCP_CREDENTIALS"]
)

credentials = service_account.Credentials.from_service_account_info(
    credentials_info
)

client = bigquery.Client(
    credentials=credentials,
    project=credentials_info["banking-etl-project"]
)

df = pd.read_csv("customer_summary.csv")

table_id = "banking-etl-project.banking_data.customer_summary"

job = client.load_table_from_dataframe(
    df,
    table_id
)

job.result()

print("Data Loaded to BigQuery Successfully!")