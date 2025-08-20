from pyspark.sql.functions import col

def transform_data(df):
    return df.withColumn("salary_in_lakhs", col("salary")/100000)