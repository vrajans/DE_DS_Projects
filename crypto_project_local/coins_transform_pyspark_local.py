from pyspark.sql import SparkSession
from pyspark.sql.functions import col
# import os
import glob

print(glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/*.csv"))

spark = SparkSession.builder.appName("CryptoDataTransformation").getOrCreate()

# os.makedirs("D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/", exist_ok=True)
# os.makedirs("D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/csv/crypto/", exist_ok=True)

api_path = glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/*.csv")
csv_path = glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/csv/crypto/*.csv")

df_api = spark.read.csv(api_path, header=True, inferSchema=True)
df_csv = spark.read.csv(csv_path, header=True, inferSchema=True)

#df_api.show(5)
print("API rows:", df_api.count())
print("CSV rows:", df_csv.count())

df_api_std = df_api.select(col("id").alias("coin_id"),
                           col("symbol").alias("ticker"),
                           col("name").alias("coin_name"),
                           col("current_price").alias("price_usd"),
                           col("Ingestion_time").alias("load_time"))

df_csv_std = df_csv.select(col("coin_id"),  
                           col("ticker"), 
                           col("coin_name"), 
                           col("price_usd"), 
                           col("loaded_at").alias("load_time"))

df_final = df_api_std.unionByName(df_csv_std)

output_path = "D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto/"
df_final.write.mode("overwrite").csv(output_path, header=True)


