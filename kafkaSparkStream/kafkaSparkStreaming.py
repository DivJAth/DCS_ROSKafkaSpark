#!/usr/bin/env python

import sys
from json import loads
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark import SparkConf
from pyspark.streaming.kafka import KafkaUtils
from math import pow, atan2, sqrt, radians, sin, cos

from producer import *


def print_stream(x):
    print("Inside stream:",loads(x[1]).encode('utf-8'))

#sparkConf.set("spark.streaming.concurrentJobs", "2")

def euclidean_distance(curr_pos,final_pose):
    return sqrt(pow((curr_pos["x"] - final_pose["x"]), 2) +
                       pow((curr_pos["y"] - final_pose["y"]), 2))

def turn_angle(curr_pos,final_pose):
   x, y, theta = curr_pos["x"], curr_pos["y"], curr_pos["theta"]
   inc_x = final_pose['x'] - x                    
   inc_y = final_pose['y'] - y  
   angle_to_goal = atan2 (inc_y, inc_x)
   return  angle_to_goal, atan2(sin(angle_to_goal-theta), cos(angle_to_goal-theta))


def consumer_decode(msg):
    data = eval(msg[1]) 
    dist = euclidean_distance(data["curr_pose"], data["final_pose"])  
    angle_to_goal, turn  = turn_angle(data["curr_pose"], data["final_pose"])
    # print("check_decode",eval(msg[1]), type(data['curr_pose']), data['final_pose'], type(data))
    return (dist, angle_to_goal, turn)
    
       # for key,value in msg.items():
            # print(value[0]./value)
    # return (dist, angle_to_goal, turn)

def print_stream1(x):
    print("Stream2:",loads(x[1])[0]+1)

kafka_producer = connect_kafka_producer()
def handler(message):
    records = message.collect()
    for record in records:
        kafka_producer.send('spark.out', str(record))
        kafka_producer.flush()

if __name__ == "__main__":
    #conf=SparkConf.setAppName("PythonkafkaWordCount")#.set("spark.streaming.concurrentJobs", "2")
    sc=SparkContext(appName="PythonkafkaWordCount")
    ssc=StreamingContext(sc,10)
    #conf=SparkConf.set("spark.streaming.concurrentJobs", "2").setAppName("PythonkafkaWordCount")
    sc.setLogLevel("OFF")
    brokers,topic1=sys.argv[1:]
    #kvs=KafkaUtils.createStream(ssc,brokers,"Spark-streaming-consumer",{topic:1})
    kvs=KafkaUtils.createStream(ssc,brokers,"Spark-streaming-consumer",{topic1:1})
    #print("KVS:",kvs)
    #print("kvs type:",type(kvs))
    #lines=kvs.map(print_stream)
    kvs.map(consumer_decode).foreachRDD(handler)

    # publish_message(kafka_producer, 't2', 'ans', 'whatever')
    # kvs.foreachRDD(handler)

    # ssc.start()
    # ssc.awaitTermination()
    # print("tester")
    # lines1.pprint()
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
