#!/usr/bin/env python

import sys
from json import loads
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark import SparkConf
from pyspark.streaming.kafka import KafkaUtils
from math import pow, atan2, sqrt, radians, sin, cos
from pymongo import MongoClient

from producer import *
import time
import datetime


client=MongoClient('localhost', 27017)
coll=client.testTopic.te

def print_stream(x):
    print("Inside stream:",loads(x[1]).encode('utf-8'))

# sparkConf.set("spark.streaming.concurrentJobs", "2")

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
    return (dist, angle_to_goal, turn, data["curr_pose"]["theta"])
    

def print_stream1(x):
    print("Stream2:",loads(x[1])[0]+1)

kafka_producer = connect_kafka_producer()
def handler(message):
    records = message.collect()
    for record in records:
        ts=time.time()
        st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        kafka_producer.send('spark.out', str(record))
        mydict={st:record}
        z=coll.insert_one(mydict)
        # print("inserted")
        kafka_producer.flush()



if __name__ == "__main__":
    
    sc=SparkContext(appName="PythonkafkaWordCount")
    ssc=StreamingContext(sc,10)
    sc.setLogLevel("OFF")
    brokers,topic1=sys.argv[1:]
    kvs=KafkaUtils.createStream(ssc,brokers,"Spark-streaming-consumer",{topic1:1})
    kvs.map(consumer_decode).foreachRDD(handler)
    ssc.start()
    ssc.awaitTermination()
