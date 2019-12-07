from __future__ import print_function
import sys
from json import loads
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark import SparkConf
from pyspark.streaming.kafka import KafkaUtils

def print_stream(x):
    print("Inside stream:",loads(x[1])[0]+1)

#sparkConf.set("spark.streaming.concurrentJobs", "2")

def print_stream1(x):
    print("Stream2:",loads(x[1])[0]+1)

if __name__ == "__main__":
    #conf=SparkConf.setAppName("PythonkafkaWordCount")#.set("spark.streaming.concurrentJobs", "2")
    sc=SparkContext(appName="PythonkafkaWordCount")
    ssc=StreamingContext(sc,10)
    #conf=SparkConf.set("spark.streaming.concurrentJobs", "2").setAppName("PythonkafkaWordCount")
    sc.setLogLevel("OFF")
    brokers,topic=sys.argv[1:]
    #kvs=KafkaUtils.createStream(ssc,brokers,"Spark-streaming-consumer",{topic:1})
    kvs1=KafkaUtils.createStream(ssc,brokers,"Spark-streaming-consumer",{topic:1})
    #print("KVS:",kvs)
    #print("kvs type:",type(kvs))
    #lines=kvs.map(print_stream)
    lines1=kvs1.map(print_stream1)
    #print("Lines:",lines)
    #lines.pprint()
    lines1.pprint()
    #counts=lines.flatMap(lambda line: line.split(','))
    #.flatMap(lambda row: (row[0]+10,row[1]+10))
    #print("COUNTS:")
    #counts.pprint()
    
    #lines[0]=lines[0]+10
    #lines[0]=lines[1]+10
    #print("After:")
    #lines.pprint()
    #counts=lines.flatMap(lambda line:line.split(" ")).map(lambda word:(word,1)).reduceByKey(lambda a,b:a+b)
    #counts.pprint()

    ssc.start()
    ssc.awaitTermination()
