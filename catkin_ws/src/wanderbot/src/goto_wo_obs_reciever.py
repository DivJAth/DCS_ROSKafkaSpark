#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, radians, sin, cos
from getLocation import Location
from gazebo_msgs.msg import ModelStates

from producer import *
import json

consumer1 = KafkaConsumer('laser', auto_offset_reset='latest',
       bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=10000000)
 
consumer2 = KafkaConsumer('spark.out', auto_offset_reset='latest', 
        bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=10000000)

# consumer1 = KafkaConsumer('laser', auto_offset_reset='latest',
#                              bootstrap_servers=['localhost:9092'], api_version=(0, 10), consumer_timeout_ms=10000000,
#                              value_deserializer=lambda x: loads(x.decode('utf-8')))

# gazebo_loc = Location()
# curr_pos = {}
# all_obstacle_location = []
final_pose={"x":-2.923, "y":2.0433}
move_forward = False
distance_tolerance = 0.5
obstacle=False
# kafka_producer = connect_kafka_producer()
# odomval()


rospy.init_node ('wander1', anonymous=True)
pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
speed = Twist()
r = rospy.Rate(4)

while True:
        for msg2 in consumer2:
            print("Before message: distance_message", msg2.value)
        for msg in consumer1:
            print("Before message:", msg.value)
            # for msg2 in consumer2:
            #     print("Before message:", msg2.value)

            # print(xxx, curr_pos, dist, turn)
            # if abs(angle_to_goal - curr_pos["theta"]) < 0.1:    #0.1 because it too exact for a robot if both angles should be exactly 0
            #     move_forward = True
            # speed.angular.z = 0.2 * turn
            # if move_forward == True:
            #     #keep speed between 0.3 and 0.7
            #     if 0.1 * dist > 0.3 and 0.1 * dist < 0.7:
            #         speed.linear.x = 0.05 * dist
            #     elif 0.1 * dist > 0.7:
            #         speed.linear.x = 0.7
            #     else:
            #         speed.linear.x = 0.3

            # pub.publish(speed)
    
    
# odomval()





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