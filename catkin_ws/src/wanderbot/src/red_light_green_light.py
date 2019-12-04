#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from getLocation import Location


cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1) 
rospy.init_node('red_light_green_light')

red_light_twist = Twist() 
green_light_twist = Twist()
green_light_twist.linear.x = 0.5 

driving_forward = False
light_change_time = rospy.Time.now()
rate = rospy.Rate(1000)

while not rospy.is_shutdown():
    # print("here")
    if driving_forward:    
        # print("here 1")
        cmd_vel_pub.publish(green_light_twist)

        test = Location()
        print(test.update_gazebo_modelPoints()[4])
    else:
        # print("here 11")
        cmd_vel_pub.publish(red_light_twist)
    print(light_change_time, rospy.Time.now())
    if light_change_time < rospy.Time.now():     
        # print("here 2")
        driving_forward = not driving_forward
        light_change_time = rospy.Time.now() + rospy.Duration(3)  
    rate.sleep()

