import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

KAFKA_TOPIC_NAME_CONS = "testtopic"
# KAFKA_OUTPUT_TOPIC_NAME_CONS = "outputtopic"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

# sc = SparkContext(appName="PythonStreamingKafkaWordCount")
# ssc = StreamingContext(sc, 1)

spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka Demo") \
        .master("local[*]") \
        .config("spark.jars", "spark-sql-kafka-0-10_2.11-2.4.0.jar,kafka-clients-1.1.0.jar") \
        .config("spark.executor.extraClassPath", "spark-sql-kafka-0-10_2.11-2.4.0.jar:kafka-clients-1.1.0.jar") \
        .config("spark.executor.extraLibrary", "spark-sql-kafka-0-10_2.11-2.4.0.jar:kafka-clients-1.1.0.jar") \
        .config("spark.driver.extraClassPath", "spark-sql-kafka-0-10_2.11-2.4.0.jar:kafka-clients-1.1.0.jar") \
        .getOrCreate()


spark.sparkContext.setLogLevel("ERROR")

ds1 = spark.readStream().format("kafka").option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS_CONS).option("subscribe",KAFKA_TOPIC_NAME_CONS).load()
ds1.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")



print("Printing Schema of transaction_detail_df: ")
ds1.printSchema()