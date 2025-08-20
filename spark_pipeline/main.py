from pyspark.sql import SparkSession
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

def main():
    spark = SparkSession.builder \
        .appName("ETL-Pipeline") \
        .getOrCreate()

    # Extract
    df = extract_data(spark)

    # Transform
    df_transformed = transform_data(df)

    # Load
    load_data(df_transformed)

    spark.stop()

if __name__ == "__main__":
    main()