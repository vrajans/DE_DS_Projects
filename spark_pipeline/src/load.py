def load_data(df):
    df.write.mode("overwrite").parquet("data/output/")
    #.save("data/output/transformed_data.parquet")
