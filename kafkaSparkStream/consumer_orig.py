from kafka import KafkaConsumer, KafkaProducer


if _name_ == '_main_':

    print('Running Consumer..')
    topic_name = 't1'

    consumer = KafkaConsumer(topic_name, auto_offset_reset='latest',
                             bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=10000000)
    while(True):
        msg = consumer._poll_once(timeout_ms=100, max_records=1)
        if (msg):
            for key,value in msg.items():
                    print(value[0].value)