# Kafka Install
wget "http://apache-mirror.8birdsvideo.com/kafka/2.3.0/kafka_2.12-2.3.0.tgz"
tar -xzf kafka_2.12-2.3.0.tgz
#python warpper for kafka
pip install kafka-python


## Spark Install
wget https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0-bin-hadoop2.7.tgz 
tar xzvf spark-2.0.0-bin-hadoop2.7.tgz 
mv spark-2.0.0-bin-hadoop2.7/* spark    # move stuf from inside  spark-2.2.0-bin-hadoop2.7 to spark
sudo mv spark/ /usr/lib/

# Add these to ~/.bashrc
export JAVA_HOME=/usr/lib/jvm/default-java/jre
export SPARK_HOME=/usr/lib/spark
export PATH=$PATH:SPARK_HOME

## use pip to install spark
## https://spark.apache.org/downloads.html
## use spark-direct 
pip3 install pyspark

## to run spark-submit
source ~/.bashrc
#  /usr/lib/spark/bin/spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0  ~/Desktop/ROS/dsc_wanderbot/kafkaSparkStream/kafkaSparkStreaming.py localhost:2181 t1

## Mongodb Install
#install PyMongo & MongoDB:
pip install pymongo
sudo apt-get update
sudo apt-get install -y mongodb-org

#ROS Setup
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt-get install ros-kinetic-desktop-full
sudo apt-get update
sudo rosdep init
rosdep update
echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
sudo apt install python-rosinstall python-rosinstall-generator python-wstool build-essential

##Make catkin workspace
mkdir -p ~/catkin_ws/src
catkin_create_pkg catkin_ws rospy geometry_msgs sensor_msgs nav_msgs trajectory_msgs actionlib_msgs diagnostic_msgs 
cd ~/catkin_ws/
catkin_make
source devel/setup.bash

##Turtlebot
# to get the turtle bot world ready in gazebo did the following
sudo apt update && sudo apt upgrade
sudo apt-get install ros-kinetic-turtlebot-gazebo (-p1 for the patches maybe)
rosmake turtlebot_gazebo
export TURTLEBOT_GAZEBO_WORLD_FILE=/opt/ros/kinetic/share/turtlebot_gazebo/worlds/playground.world

