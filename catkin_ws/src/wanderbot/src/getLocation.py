from gazebo_msgs.srv import GetModelState, GetWorldProperties
from tf.transformations import euler_from_quaternion
import rospy
from geometry_msgs.msg import Twist, Pose, Point

class Block:
    def __init__(self, name, relative_entity_name):
        self._name = name
        self._relative_entity_name = relative_entity_name

class Location:
    _blockListDict = {
    'a': Block('jersey_barrier', 'link'),
        'b': Block('unit_cylinder_1', 'link'),
        # 'b1': Block('unit_cylinder_1_clone', 'link'),
        'c': Block('ground_plane_0', 'link'),
        'd': Block('mobile_base', 'link'),
        # 'd1': Block('mobile_base_clone', 'link'),
        'e': Block('cube_20k', 'link'),
        # 'f': Block('turtlebot', 'link')
        # 'e1': Block('cube_20k_clone', 'link'),
    
    }
    def update_gazebo_modelPoints(self):
        try:
            plist = []
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state',GetModelState)
            for block in self._blockListDict.itervalues():
                blockName = str(block._name)
                resp_coordinates = model_coordinates(blockName,"")
                rot_q = resp_coordinates.pose.orientation
                (roll,pitch,theta) = euler_from_quaternion ([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
                # print([Point(resp_coordinates.pose.position.x,
                    # resp_coordinates.pose.position.y,resp_coordinates.pose.position.z),{"theta":theta}])
                plist.append({blockName:{"x":resp_coordinates.pose.position.x,"y":resp_coordinates.pose.position.y,
                    "z":resp_coordinates.pose.position.z, "theta":theta}})
            return plist
        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))



# if __name__ == '__main__':
#     x=Location()
#     print("s1",x.update_gazebo_modelPoints())
#     # sleep(3)
#     # print("s2",x.update_gazebo_modelPoints())