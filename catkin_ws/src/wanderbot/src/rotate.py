#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist
import math
from math import radians

from getLocation import Location

test = Location()
print(test.update_gazebo_modelPoints())

roll = pitch = yaw = 0.0
target = 30
kp=0.5

def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    # print(roll, pitch, yaw)

rospy.init_node('rotate_robot')

sub = rospy.Subscriber ('/odom', Odometry, get_rotation)
pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
r = rospy.Rate(10)
command =Twist()
command.linear.x = 0.2
# print(radians(90))
while not rospy.is_shutdown():
    #quat = quaternion_from_euler (roll, pitch,yaw)
    #print quat
    target_rad = radians(target)
    command.angular.z = kp * (target_rad-yaw)
    print(target_rad, command.angular.z)

    pub.publish(command)
    r.sleep()
    print("here",test.update_gazebo_modelPoints())
    for i in range(0,10):        
        pub.publish(command)
        r.sleep()



    print("taeget={} current:{}", target,yaw)
    r.sleep()