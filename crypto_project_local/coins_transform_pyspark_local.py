# -----------------------------
# Import Libraries & Start Spark
# -----------------------------
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month, dayofmonth, avg, max, min, lag, stddev,sum as _sum, rank, desc, row_number, first, last, when, date_format, weekofyear, dayofweek, quarter, lit
from pyspark.sql.window import Window
import glob
from dotenv import load_dotenv
import os
import pyodbc as pyodb

# Load environment variables from .env file
load_dotenv("D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/env_var.env")

server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")


#print(glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/*.csv"))

# Initialize Spark session
spark = (SparkSession.builder
         .appName("CryptoDataTransformation")
         .getOrCreate()
         )

# os.makedirs("D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/", exist_ok=True)
# os.makedirs("D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/csv/crypto/", exist_ok=True)

# -----------------------------
# Load CSV Data
# -----------------------------

# file paths
#api_path = glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/api/crypto/*.csv")
csv_path = glob.glob(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/raw/csv/crypto/*.csv")

#df_api = spark.read.csv(api_path, header=True, inferSchema=False)
df = spark.read.csv(csv_path, header=True, inferSchema=True)

# Show sample
#df_api.show(5)
df.show(5)
#df_api.printSchema()
df.printSchema()
#print("API rows:", df_api.count())
print("CSV rows:", df.count())

# -----------------------------
# Data Cleaning
# -----------------------------

# Drop duplicates
#df_api = df_api.dropDuplicates()
df = df.dropDuplicates()

# Handle missing values (replace with 0)
df = df.fillna({'open': 0, 'close': 0, 'high': 0, 'low': 0, 'volume': 0})

# -----------------------------
# Date/Time Transformations
# -----------------------------
df = df.withColumn('year', year(col('date')))
df = df.withColumn('month', month(col('date')))
df = df.withColumn('day', dayofmonth(col('date')))


# -----------------------------
# Price & Volume Features
# -----------------------------
# Daily price change
df = df.withColumn('price_change', col('close') - col('open'))
df = df.withColumn('price_change_pct', (col('close') - col('open')) / col('open') * 100)

# High-Low difference
df = df.withColumn('high_low_diff', col('high') - col('low'))

# 7-day moving average of closing price
window_7 = Window.partitionBy('symbol').orderBy('date').rowsBetween(-6, 0)
df = df.withColumn('ma_7', avg('close').over(window_7))

# 30-day rolling standard deviation (volatility)
window_30 = Window.partitionBy('symbol').orderBy('date').rowsBetween(-29, 0)
df = df.withColumn('volatility_30', stddev('close').over(window_30))

# -----------------------------
# Lag/Shift Features
# -----------------------------
window_spec = Window.partitionBy('symbol').orderBy('date')

# Previous day close
df = df.withColumn('prev_close', lag('close', 1).over(window_spec))

# Previous day price change
df = df.withColumn('prev_price_change', col('close') - col('prev_close'))

# -----------------------------
# Aggregations / Monthly Summary
# -----------------------------
monthly_stats = df.groupBy('symbol', 'year', 'month').agg(
    max('close').alias('max_close'),
    min('close').alias('min_close'),
    avg('close').alias('avg_close'),
    avg('volume').alias('avg_volume')
)

# -----------------------------
# Flags / Labels
# -----------------------------
df = df.withColumn('high_volume_flag', (col('volume') > 1_000_000).cast('integer'))
df = df.withColumn('price_spike_flag', (col('price_change_pct') > 5).cast('integer'))


# Standardize column names and select relevant columns

# df_api_std = df_api.select(col("id").alias("coin_id"),
#                            col("symbol").alias("ticker"),
#                            col("name").alias("coin_name"),
#                            col("current_price").alias("price_usd"),
#                            col("Ingestion_time").alias("load_time"))

# df_csv_std = df.select(col("SNo").alias("coin_id"),
#                            col("Symbol").alias("ticker"),
#                            col("Name").alias("coin_name"),
#                            col("Close").alias("price_usd"),
#                            col("Date").alias("load_time"))

# df_final = df_api_std.unionByName(df_csv_std)

# print("CSV rows:", df_final.count())

# -----------------------------
# Save Transformed Data
# -----------------------------
# Save locally as Parquet (optimized for analytics)
output_path = r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto"
df.write.mode('overwrite').parquet(output_path)

# -----------------------------
# Optional: Push to SQL Server
# -----------------------------

# JDBC connection URL for SQL Server
jdbc_url = f"jdbc:sqlserver://{server};databaseName={database};user={username};password={password}"

# Table name in SQL Server
table_name = "TransformedCrypto"

# Write the DataFrame to csv file
# output_path = "D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto/"
# df_final.coalesce(1).write.mode("overwrite").csv(output_path, header=True)
#print("Final CSV written to:", output_path + "/crypto_data.csv")

# Write to SQL Server
df.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", table_name) \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()

print(f"Data successfully written to SQL Server table: {table_name}")


# -----------------------------
# Cumulative Returns
# -----------------------------
# (close / first close) - 1
window_cum = Window.partitionBy("symbol").orderBy("date") \
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df = df.withColumn("cumulative_return",
                   (col("close") / first("close").over(window_cum) - 1) * 100)

# -----------------------------
# Daily Top Gainers / Losers
# -----------------------------
daily_rank = Window.partitionBy("date").orderBy(desc("price_change_pct"))
df = df.withColumn("daily_rank_gain", rank().over(daily_rank))

# Top 5 gainers
top_gainers = df.filter(col("daily_rank_gain") <= 5)

# Top 5 losers
daily_rank_loss = Window.partitionBy("date").orderBy(col("price_change_pct"))
df = df.withColumn("daily_rank_loss", rank().over(daily_rank_loss))
top_losers = df.filter(col("daily_rank_loss") <= 5)

# -----------------------------
# Multi-Coin Comparison
# -----------------------------
# Compare average monthly returns between coins
coin_comparison = df.groupBy("symbol", "year", "month") \
    .agg(avg("price_change_pct").alias("avg_monthly_return"),
         avg("volume").alias("avg_monthly_volume"))

# -----------------------------
# Portfolio-style Summary
# -----------------------------
portfolio_summary = df.groupBy("symbol") \
    .agg(
        avg("close").alias("avg_price"),
        max("close").alias("max_price"),
        min("close").alias("min_price"),
        _sum("volume").alias("total_volume")
    ) \
    .orderBy(desc("total_volume"))

# -----------------------------
# Save Advanced Outputs
# -----------------------------
# Save advanced results in parquet
df.write.mode("overwrite").parquet(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto")

top_gainers.write.mode("overwrite").parquet(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto")
top_losers.write.mode("overwrite").parquet(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto")
coin_comparison.write.mode("overwrite").parquet(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto")
portfolio_summary.write.mode("overwrite").parquet(r"D:/Varath/DE_DS/DE_DS_Projects/crypto_project_local/csvdata/processed/crypto")

# -----------------------------
# Push Advanced Results to SQL Server
# -----------------------------
# Example: Save Top Gainers to SQL Server

top_gainers.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "TopGainers") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()

top_losers.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "TopLosers") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()

portfolio_summary.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "PortfolioSummary") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()


ohlc_df = df.groupBy("symbol", "date").agg(
    first("close").alias("open_price"),
    max("close").alias("high_price"),
    min("close").alias("low_price"),
    last("close").alias("close_price"),
    _sum("volume").alias("daily_volume")
)


volatility_df = df.groupBy("symbol", "year", "month") \
    .agg(stddev("price_change_pct").alias("monthly_volatility"))


df = df.withColumn("gain", when(col("price_change_pct") > 0, col("price_change_pct")).otherwise(0))
df = df.withColumn("loss", when(col("price_change_pct") < 0, -col("price_change_pct")).otherwise(0))

window14 = Window.partitionBy("symbol").orderBy("date").rowsBetween(-13, 0)

df = df.withColumn("avg_gain", avg("gain").over(window14))
df = df.withColumn("avg_loss", avg("loss").over(window14))

df = df.withColumn("rs", col("avg_gain") / col("avg_loss"))
df = df.withColumn("rsi_14d", 100 - (100 / (1 + col("rs"))))



# Save OHLC to SQL Server
ohlc_df.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "CoinOHLC") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()



# Save Moving Averages
df.select("symbol", "date", "close", "ma_7d", "ma_30d") \
    .write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "CoinMovingAverages") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()

# Save Volatility 
volatility_df.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "CoinVolatility") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()


df = df.withColumn("date", col("date").cast("date"))

dim_date = df.select("date").distinct() \
    .withColumn("DateID", date_format("date", "yyyyMMdd").cast("int")) \
    .withColumn("Year", year("date")) \
    .withColumn("Month", month("date")) \
    .withColumn("MonthName", date_format("date", "MMMM")) \
    .withColumn("Quarter", quarter("date")) \
    .withColumn("WeekOfYear", weekofyear("date")) \
    .withColumn("DayOfWeek", date_format("date", "EEEE")) \
    .withColumnRenamed("date", "FullDate")

dim_coin = df.select("symbol", "coin_name").distinct() \
    .withColumn("Category", lit("Crypto")) \
    .withColumn("LaunchYear", lit(2009)) \
    .withColumn("MarketCapRank", lit(None).cast("int")) \
    .withColumnRenamed("symbol", "Symbol") \
    .withColumnRenamed("coin_name", "CoinName")

ohlc_df = df.groupBy("symbol", "date").agg(
    first("close").alias("OpenPrice"),
    max("close").alias("HighPrice"),
    min("close").alias("LowPrice"),
    last("close").alias("ClosePrice"),
    _sum("volume").alias("DailyVolume"),
    avg("price_change_pct").alias("PriceChangePct"),
    avg("ma_7d").alias("MA7D"),
    avg("ma_30d").alias("MA30D"),
    avg("rsi_14d").alias("RSI14D"),
    avg("cumulative_return").alias("CumulativeReturn")
)

fact_crypto = ohlc_df \
    .withColumn("DateID", date_format("date", "yyyyMMdd").cast("int")) \
    .withColumnRenamed("symbol", "Symbol")

dim_date.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "DimDate") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()

dim_coin.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "DimCoin") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()


fact_crypto.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", jdbc_url) \
    .option("dbtable", "FactCryptoPrices") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .option("encrypt", "true") \
    .option("trustServerCertificate", "true") \
    .save()