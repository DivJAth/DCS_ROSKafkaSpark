#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt, radians, sin, cos
from getLocation import Location
from gazebo_msgs.msg import ModelStates


gazebo_loc = Location()
curr_pos = {}
all_obstacle_location = []
final_pose={"x":-2.923, "y":2.0433}

g_range_ahead = 1 # anything to start
scan_sub = rospy.Subscriber('scan', LaserScan, scan_callback)

move_forward = False
# def euclidean_distance(curr_pos,final_pose):
#     return sqrt(pow((curr_pos["x"] - final_pose["x"]), 2) +
#                        pow((curr_pos["y"] - final_pose["y"]), 2))
def odomval():
    global curr_pos, all_obstacle_location
    all_obstacle_location =  gazebo_loc.update_gazebo_modelPoints()
    curr_pos = all_obstacle_location[4]["mobile_base"] 

# def obstacle_check(msg):
#     global g_range_ahead
#     g_range_ahead = min(msg.ranges)
#     if g_range_ahead < 0.8:
#         return True
#     return False

# def turn_angle(curr_pos,final_pose):
#     x, y, theta = curr_pos["x"], curr_pos["y"], curr_pos["theta"]
#     inc_x = final_pose['x'] - x                    
#     inc_y = final_pose['y'] - y  
#     angle_to_goal = atan2 (inc_y, inc_x)
#     return  angle_to_goal, atan2(sin(angle_to_goal-theta), cos(angle_to_goal-theta))

# def linear_vel(curr_pos, final_pose, constant = 1):
#     return constant * euclidean_distance(curr_pos,final_pose)

# def angular_vel(goal_pose, final_pose, constant = 0.1):
#     return constant * (steering_angle(curr_pos, final_pose) - curr_pos["theta"])

    
distance_tolerance = 0.5
odomval()
xxx = 0

rospy.init_node ('wander', anonymous=True)
pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=1)

speed = Twist()
r = rospy.Rate(4)

obstacle=False
kafka_producer = connect_kafka_producer()
while (euclidean_distance(curr_pos, final_pose) > distance_tolerance):
    # x, y, theta = curr_pos["x"], curr_pos["y"], curr_pos["theta"]
    # inc_x = final['x'] - x                    #distance robot to goal in x
    # inc_y = final['y'] - y                      #distance robot to goal in y
    # angle_to_goal = atan2 (inc_y, inc_x)    #calculate angle through distance from robot to goal in x and y
    # dist = sqrt(pow(inc_x, 2) + pow(inc_y, 2))      #calculate distance
    if obstacle:
        xxx += 1  
    else:
        dist = euclidean_distance(curr_pos, final_pose)
        #find out which turndirection is better
        # the bigger the angle, the bigger turn, - when clockwise
        # turn = atan2(sin(angle_to_goal-theta), cos(angle_to_goal-theta))
        angle_to_goal, turn = turn_angle(curr_pos,final_pose)
    
    print(xxx, curr_pos, dist, turn)

    if abs(angle_to_goal - curr_pos["theta"]) < 0.1:    #0.1 because it too exact for a robot if both angles should be exactly 0
        move_forward = True

    speed.angular.z = 0.2 * turn

    if move_forward == True:
        #keep speed between 0.3 and 0.7
        if 0.1 * dist > 0.3 and 0.1 * dist < 0.7:
            speed.linear.x = 0.05 * dist
        elif 0.1 * dist > 0.7:
            speed.linear.x = 0.7
        else:
            speed.linear.x = 0.3

    pub.publish(speed)
    odomval()