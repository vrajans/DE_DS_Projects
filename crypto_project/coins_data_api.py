import requests
import pandas as pd
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()


url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 250,
    "page": 1,
    "sparkline": "false"
}

response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data)
df["ingestion_time"] = datetime.now()

# Save DataFrame to CSV in memory
csv_data = df.to_csv(index=False)

# Upload to Azure Blob Storage
connection_string = os.getenv("CONNECTION_STR")
container_name = os.getenv("AZURE_CONTAINER")

# Define the blob (file) name and folder structure with timestamp
file_name = f"raw/api/crypto/crypto_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Create blob service client
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

#create container client
container_client = blob_service_client.get_container_client(container_name)

# Upload the CSV data
container_client.upload_blob(name=file_name, data=csv_data, overwrite=True)

print(f"Uploaded {file_name} to {container_name} container")