#Launch TurtleBot
roslaunch turtlebot_gazebo turtlebot_world.launch

cd kafka_2.12-2.3.0
#run zookeeper in the kafka_2.12-2.3.0
bin/zookeeper-server-start.sh config/zookeeper.properties

#run the kafka server
bin/kafka-server-start.sh config/server.properties

# Run Spark
$SPARK_HOME/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  ~/Desktop/ROS/dsc_wanderbot/kafkaSparkStream/kafkaSparkStreaming.py localhost:2181 t1

# Run MongoDB
#start mongod server
sudo service mongod start
#check the status
sudo service mongod status

# Start ROS NODES
src/wanderbot/src/goto_obs_reciever.py 
src/wanderbot/src/goto_obs_sender.py 
