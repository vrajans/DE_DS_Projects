import requests
import pandas as pd
from datetime import datetime

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
df.to_csv(f"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/crypto_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", index=False)