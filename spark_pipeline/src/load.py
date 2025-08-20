def load_data(df):
    df.write.mode("overwrite").parquet("data/output/")