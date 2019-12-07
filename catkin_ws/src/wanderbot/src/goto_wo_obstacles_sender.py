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

rospy.init_node ('wander', anonymous=True)
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)

# pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
# speed = Twist()
r = rospy.Rate(4)
print(euclidean_distance(curr_pos,final_pose) )
while euclidean_distance(curr_pos,final_pose) > distance_tolerance:
    print(scan_sub)
    print("send_message")
    publish_message(kafka_producer, 'dist_stuff', 'movement', {"curr_pose":curr_pos,"final_pose":final_pose})
    # kafka_producer.send('t1', value={"curr_pose":curr_pos,"final_pose":final_pose})
    kafka_producer.flush()
    print("lase_sender",g_range_ahead)
    publish_message(kafka_producer, 'laser', 'laserscan', {"distance_obstacle": g_range_ahead})
    sleep(10)
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

    
