#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, radians, sin, cos, isnan
from getLocation import Location
from numpy import nan
# from gazebo_msgs.msg import ModelStates

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


rospy.init_node ('wander', anonymous=True)
pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)
speed = Twist()
r = rospy.Rate(4)

while True:
    msg_obstacle = consumer1._poll_once(timeout_ms=10, max_records=1)
    if (msg_obstacle):
        for key1, msg1 in msg_obstacle.items():
            # print("consumer1", msg1[0].value, type(msg1[0].value))
            if not (msg1[0].value == 'nan'):
                # print("enter", (msg1[0].value), type(eval(msg1[0].value)))
                obs_dist =eval(msg1[0].value)
                if obs_dist["distance_obstacle"] < 0.8:
                    print("Obstacle Ahead")
                    break
                   
    msg_movement = consumer2._poll_once(timeout_ms=100, max_records=10)
    if (msg_movement):
        for key2, msg2 in msg_movement.items():
            print("Before message: distance_message", eval(msg2[0].value))
            movement = eval(msg2[0].value)
            dist, angle_to_goal, turn, original_theta = movement[0], movement[1], movement[2], movement[3]
            print(abs(angle_to_goal - original_theta))
            if abs(angle_to_goal - original_theta) < 0.1:    #0.1 because it too exact for a robot if both angles should be exactly 0
                print("here")
                move_forward = True
            speed.angular.z = 0.2 * turn
            if move_forward == True:
                #keep speed between 0.3 and 0.7
                print("move_forward")
                if 0.1 * dist > 0.3 and 0.1 * dist < 0.7:
                    speed.linear.x = 0.05 * dist
                elif 0.1 * dist > 0.7:
                    speed.linear.x = 0.7
                else:
                    speed.linear.x = 0.3
                print("move_forward", speed.linear.x)
            pub.publish(speed)

