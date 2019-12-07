#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, radians
from getLocation import Location

test = Location()
curr_pos = {}
final={"x":-2.923, "y":2.0433}

# curr_y = 0.0
# curr_theta = 0.0

def scan_callback(msg):
    global g_range_ahead
    g_range_ahead = min(msg.ranges)

def odomval():
    global curr_pos
    curr_pos = test.update_gazebo_modelPoints()[4]["mobile_base"] 
    # print("curr_position",curr_pos)
    # print("from getloc",test.update_gazebo_modelPoints()[4]["mobile_base"])

def euclidean_distance(curr_pos,final_pose):
    return sqrt(pow((curr_pos["x"] - final_pose["x"]), 2) +
                       pow((curr_pos["y"] - final_pose["y"]), 2))

def linear_vel(curr_pos, final_pose, constant = 1):
    return constant * euclidean_distance(curr_pos,final_pose)

def steering_angle(curr_pos,final_pose):
    return atan2(final_pose["y"] - curr_pos["y"], final_pose["x"] - curr_pos["x"])

def angular_vel(goal_pose, final_pose, constant = 0.1):
    return constant * (steering_angle(curr_pos, final_pose) - curr_pos["theta"])

rospy.init_node('wander', anonymous=True)

g_range_ahead = 1 # anything to start
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)
cmd_vel_pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size=1)
# pose_subscriber = rospy.Subscriber('/odom', Odometry, odom_callback)
rate = rospy.Rate(10)


# state_change_time = rospy.Time.now()
driving_forward = True
distance_tolerance = 2
odomval()
xxx=0
k=0.2
while (euclidean_distance(curr_pos, final) > distance_tolerance) or xxx>20:
    xxx+=1
    odomval()
    # if driving_forward:
    #     if (g_range_ahead < 0.1):
    #         driving_forward = False
    #         # state_change_time = rospy.Time.now() + rospy.Duration(5)
    # else: # we're not driving_forward
    #     # if rospy.Time.now() > state_change_time:
    #     driving_forward = True # we're done spinning, time to go forward!
    #     # state_change_time = rospy.Time.now() + rospy.Duration(30)
    
    twist = Twist()
    if driving_forward:
        print(curr_pos,final,linear_vel(curr_pos, final),euclidean_distance(curr_pos, final),angular_vel(curr_pos, final))
        twist.linear.x = linear_vel(curr_pos, final,0.5)
        twist.angular.z = 0
        # twist.angular.z = angular_vel(curr_pos, final,0.1)

    else:
        twist.linear.x = 0
        twist.angular.z = angular_vel(curr_pos, final,1)

    cmd_vel_pub.publish(twist)
    # print("here",test.update_gazebo_modelPoints()[4])
    rate.sleep()