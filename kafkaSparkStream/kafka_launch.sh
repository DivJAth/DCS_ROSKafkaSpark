wget "http://apache-mirror.8birdsvideo.com/kafka/2.3.0/kafka_2.12-2.3.0.tgz"
tar -xzf kafka_2.12-2.3.0.tgz
cd kafka_2.12-2.3.0

#run zookeeper in the kafka_2.12-2.3.0
bin/zookeeper-server-start.sh config/zookeeper.properties

#run the kafka server
bin/kafka-server-start.sh config/server.properties

#python warpper for kafka
pip install kafka-python

## run consumer and producer on the cmd
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic t1
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic t1


##Use Spark direct approach: because the is a one to one partition between the the afka topics and the spark rdd partition
## use pip to install spark
## https://spark.apache.org/downloads.html
## use spark-direct 

pip3 install pyspark



# Spark install
wget https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-hadoop2.7.tgz 
tar xzvf spark-2.0.0-bin-hadoop2.7.tgz 
mv spark-2.0.0-bin-hadoop2.7/* spark    # move stuf from inside  spark-2.2.0-bin-hadoop2.7 to spark
sudo mv spark/ /usr/lib/

# Add these to ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/default-java/jre
export SPARK_HOME=/usr/lib/spark
export PATH=$PATH:SPARK_HOME

## to run spark-submit
source ~/.bashrc
 /usr/lib/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  ~/Desktop/ROS/dsc_wanderbot/kafkaSparkStream/kafkaSparkStreaming.py localhost:2181 t1
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  ~/Desktop/ROS/dsc_wanderbot/kafkaSparkStream/kafkaSparkStreaming.py localhost:2181 t1
 



## experiments

## get spark version 
$SPARK_HOME/bin/spark-submit --version
version 2.4.4

## Kafka version
kafka_2.12-2.3.0.tgz 
