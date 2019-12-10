#!/usr/bin/env python

from time import sleep
from json import dumps
from kafka import KafkaProducer, KafkaConsumer
import json


def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key).encode('utf-8')
        value_bytes = bytes(value).encode('utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.',topic_name)
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))


def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))

        # _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

if __name__ == '__main__':


    kafka_producer = connect_kafka_producer()
    
    publish_message(kafka_producer, key, 'raw', 'message')

    if kafka_producer is not None:
        kafka_producer.close()


# def publish_message(producer_instance, topic_name, key, value):
#     try:
#         key_bytes = bytes(key).encode('utf-8')
#         value_bytes = bytes(value).encode('utf-8')
#         producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
#         producer_instance.flush()
#         print('Message published successfully.')
#     except Exception as ex:
#         print('Exception in publishing message')
#         print(str(ex))

## Sravanth
# def connect_kafka_producer():
#     _producer = None
#     try:
#         _producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10),value_serializer=lambda x: dumps(x).encode('utf-8'))
#     except Exception as ex:
#         print('Exception while connecting Kafka')
#         print(str(ex))
#     finally:
#         return _producer

# if __name__ == '__main__':
#     kafka_producer = connect_kafka_producer()
#     # publish_message(kafka_producer, 't2', 'raw', 'message')
#     cur = 0
#     final = 10
#     for i in range(1,10,1):
#         data = [i*10, i]
#         data1 = [i*5,i]
#         kafka_producer.send('testTopic', value=data)
#         kafka_producer.send('topic2',value=data1)
#         kafka_producer.flush()
#         sleep(10)


