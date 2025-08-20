def extract_data(spark):
    return spark.read.csv("data/input.csv", header=True, inferSchema=True)