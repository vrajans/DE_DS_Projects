from pyspark.sql import SparkSession
from pyspark.sql.functions import col

storage_account_name = "conitrendsdatasetvarath"
storage_account_key = "uXMe+TFGY2YCQj73N3zyYU49CDrKmTDchNmsBLr6+0CKoTwhnNVae7XUkOesqVC8sJaj8WKp+MK7+AStC/cuuA=="
container_name = "csvdata"

spark = SparkSession.builder.appName("CryptoDataTransformation").getOrCreate()

spark.conf.set(f"fs.azure.account.key.{storage_account_name}.blob.core.windows.net", storage_account_key)

api_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/raw/api/crypto/*.csv"

csv_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/raw/csv/crypto/*.csv"

df_api = spark.read.csv(api_path, header=True, inferSchema=True)
df_csv = spark.read.csv(csv_path, header=True, inferSchema=True)

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

output_path = f"wasbs://{container_name}@{storage_account_name}.blob.core.windows.net/processed/crypto/"
df_final.write.mode("overwrite").csv(output_path, header=True)
