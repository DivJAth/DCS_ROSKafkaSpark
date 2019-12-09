#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, radians, sin, cos
from getLocation import Location
from gazebo_msgs.msg import ModelStates

from producer import *

def euclidean_distance(curr_pos,final_pose):
    return sqrt(pow((curr_pos["x"] - final_pose["x"]), 2) +
                       pow((curr_pos["y"] - final_pose["y"]), 2))

def odomval():
    global curr_pos, all_obstacle_location
    all_obstacle_location =  gazebo_loc.update_gazebo_modelPoints()
    curr_pos = all_obstacle_location[4]["mobile_base"] 

def scan_callback(msg):
    global g_range_ahead
    g_range_ahead = min(msg.ranges)


gazebo_loc = Location()
curr_pos = {}
all_obstacle_location = []

final_pose={"x":-2.923, "y":2.0433}
move_forward = False
distance_tolerance = 0.5
obstacle=False
kafka_producer = connect_kafka_producer()
odomval()
g_range_ahead = 1

rospy.init_node ('wander', anonymous=True, log_level=rospy.DEBUG)
scan_topic = 'scan'
scan_sub = rospy.Subscriber(scan_topic, LaserScan, scan_callback)
rospy.loginfo("Subcribe to the topic %s", scan_topic)
# pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
# speed = Twist()
r = rospy.Rate(4)
print(euclidean_distance(curr_pos,final_pose) )
while euclidean_distance(curr_pos,final_pose) > distance_tolerance:
    # print(scan_sub)
    # print("send_message")
    print({"curr_pose":curr_pos,"final_pose":final_pose})
    kafka_topic = 'dist_stuff'
    publish_message(kafka_producer, kafka_topic, 'movement', {"curr_pose":curr_pos,"final_pose":final_pose})
    rospy.loginfo_throttle(120, "publish message to kafka on topic:"+ str(kafka_topic))
    # kafka_producer.send('t1', value={"curr_pose":curr_pos,"final_pose":final_pose})
    # print("lase_sender",g_range_ahead)
    laser_topic = 'laser'
    publish_message(kafka_producer, laser_topic, 'laserscan', {"distance_obstacle": g_range_ahead})
    rospy.loginfo_throttle(120,"publish message to kafka on topic "+ str(laser_topic))
    
    kafka_producer.flush()
    odomval()






# g_range_ahead = 1 # anything to start
# scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)

# def obstacle_check(msg):
#     global g_range_ahead
#     g_range_ahead = min(msg.ranges)
#     if g_range_ahead < 0.8:
#         return True
#     return False

#
# def linear_vel(curr_pos, final_pose, constant = 1):
#     return constant * euclidean_distance(curr_pos,final_pose)

# def angular_vel(goal_pose, final_pose, constant = 0.1):
#     return constant * (steering_angle(curr_pos, final_pose) - curr_pos["theta"])

    
