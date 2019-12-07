#!/usr/bin/env python

from kafka import KafkaConsumer, KafkaProducer
from json import loads

if __name__ == '__main__':

    print('Running Consumer..')
    topic_name = 'testTopic'

    consumer = KafkaConsumer(topic_name, auto_offset_reset='latest',
                             bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=10000000,
                             value_deserializer=lambda x: loads(x.decode('utf-8')))
    while(True):
        # msg = consumer._poll_once(timeout_ms=100, max_records=1)
        # if (msg):
        #     for key,value in msg.items():
        #             print(value[0].value)
        for msg in consumer:
            print("Before message:", msg.value)
	    msg1=msg.value
            msg1[0]=msg1[0]+10
            msg1[1]=msg1[1]+10
            print("After message:", msg1)
