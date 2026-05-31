import pandas as pd
from google.cloud import bigquery

# Service Account Key
client = bigquery.Client.from_service_account_json(
    "credentials/airflow-key.json"
)

# Read transformed file
df = pd.read_csv(
    "data/customer_summary.csv"
)

table_id = "banking-etl-project.banking_data.customer_summary"

job = client.load_table_from_dataframe(
    df,
    table_id
)

job.result()

print("Data Loaded to BigQuery Successfully!")