import sys
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.context import SQLContext

if __name__ == '__main__':
    # topic = self._randomTopic()
    # sendData = {"a": 3, "b": 5, "c": 10}

    # self._kafkaTestUtils.createTopic(topic)
    # self._kafkaTestUtils.sendMessages(topic, sendData)

    # stream = KafkaUtils.createStream(self.ssc, self._kafkaTestUtils.zkAddress(),
    #                                      "test-streaming-consumer", {topic: 1},
    #                                      {"auto.offset.reset": "smallest"})
    # self._validateStreamResult(sendData, stream)

    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingKafkaWordCount")
    ssc = StreamingContext(sc, 1)
    # _kafkaTestUtils = ssc._jvm.or?g.apache.spark.streaming.kafka.KafkaTestUtils()
    # _kafkaTestUtils.setup()

    # print(ssc._sc)

    zkQuorum, topic = sys.argv[1:]

    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    lines = kvs.map(lambda x: x[1])
    # lines.pprint()

    counts = lines.flatMap(lambda line: line.split(" ")) \
                  .map(lambda word: (word, 1)) \
                  .reduceByKey(lambda a, b: a+b)
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()