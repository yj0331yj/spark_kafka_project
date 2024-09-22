from pyspark.sql import SparkSession
from pyspark.sql.protobuf.functions import from_protobuf
import pyspark.sql.functions as F

if __name__ == "__main__":
    ss: SparkSession = SparkSession.builder \
        .master("local") \
        .appName('book_ex') \
        .config("spark.hadoop.fs.defaultFS", "local") \
        .getOrCreate()

    proto_desc_path = "/Users/jeong-yoonjin/yeardream/realtime/spark_kafka_project/proto/book_data.desc"

    df = ss.readStream \
        .format("kafka") \
        .option("startingOffset", "earliest") \
        .option("subscribe", "book") \
        .option("kafka.bootstrap.servers", "localhost:29092") \
        .load() \
        .select(from_protobuf("value", "Book", proto_desc_path).alias("book")) \
        .withColumn("title", F.col("book.title")) \
        .withColumn("author", F.col("book.author")) \
        .withColumn("publisher", F.col("book.publisher")) \
        .withColumn("price", F.col("book.price")) \
        .withColumn("publication_date", F.col("book.publication_date")) \
        .withColumn("source", F.col("book.source")) \
        .withColumn("processing_time", F.current_timestamp()) \
        .select("title", "author", "publisher", "price", "publication_date", "source", "processing_time")

    price_stat_df = df.groupby(
        F.window(F.col("processing_time"), "1 minute"), "source").agg(
        F.max("price").alias("max_price"),
        F.min("price").alias("min_price"),
        F.mean("price").alias("mean_price")
    )

    price_stat_df.writeStream \
        .format("console") \
        .outputMode("complete") \
        .option("truncate", "false") \
        .option("checkpointLocation", "/Users/jeong-yoonjin/yeardream/realtime/spark_kafka_project/checkpoint") \
        .start() \
        .awaitTermination()