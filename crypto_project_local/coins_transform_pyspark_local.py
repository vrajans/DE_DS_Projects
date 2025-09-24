from pyspark.sql import SparkSession
from pyspark.sql.functions import col
# import os
import glob

print(glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/*.csv"))

spark = (SparkSession.builder.appName("CryptoDataTransformation").config("spark.hadoop.io.nativeio.disable", "true").getOrCreate())

# os.makedirs("D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/", exist_ok=True)
# os.makedirs("D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/csv/crypto/", exist_ok=True)

api_path = glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/*.csv")
csv_path = glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/csv/crypto/*.csv")

df_api = spark.read.csv(api_path, header=True, inferSchema=False)
df_csv = spark.read.csv(csv_path, header=True, inferSchema=False)

#df_api.show(5)
print("API rows:", df_api.count())
print("CSV rows:", df_csv.count())

df_api_std = df_api.select(col("id").alias("coin_id"),
                           col("symbol").alias("ticker"),
                           col("name").alias("coin_name"),
                           col("current_price").alias("price_usd"),
                           col("Ingestion_time").alias("load_time"))

df_csv_std = df_csv.select(col("SNo").alias("coin_id"),
                           col("Symbol").alias("ticker"),
                           col("Name").alias("coin_name"),
                           col("Close").alias("price_usd"),
                           col("Date").alias("load_time"))

df_final = df_api_std.unionByName(df_csv_std)

print("CSV rows:", df_final.count())

output_path = "D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto/"
df_final.write.mode("overwrite").csv(output_path, header=True)


