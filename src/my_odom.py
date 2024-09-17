#!/usr/bin/env python3

import rospy
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point 
from tf.transformations import euler_from_quaternion

class MyOdom:
    def __init__(self):
        self.odom_sub = rospy.Subscriber('odom', Odometry, self.odom_cb)
        self.my_odom_pub = rospy.Publisher('my_odom', Point, queue_size=1)
        self.old_pose = None #updates after to get diff between distances
        self.dist = 0.0 #this represents the total distance the bot travelled
        self.yaw = 0.0 #this should represent where its pointing towards
                
    def odom_cb(self, msg):
        """Callback function for `odom_sub`."""
        cur_pose = msg.pose.pose
        self.update_dist(cur_pose) 
        self.update_yaw(cur_pose.orientation)
        self.publish_data()

    def update_dist(self, cur_pose):
        """
        Helper to `odom_cb`.
        Updates `self.dist` to the distance between `self.old_pose` and
        `cur_pose`.
        """
        if self.old_pose is None:
            self.old_pose = cur_pose.position
        else:
            x = cur_pose.position.x - self.old_pose.x
            y = cur_pose.position.y - self.old_pose.y
            dista = math.sqrt(x**2 + y**2)
            self.dist += dista
            self.old_pose = cur_pose.position
        
    def update_yaw(self, cur_orientation):
        """
        Helper to `odom_cb`.
        Updates `self.yaw` to current heading of robot.
        """
        orientation_list = [cur_orientation.x, cur_orientation.y, cur_orientation.z, cur_orientation.w]
        euler_angles = euler_from_quaternion(orientation_list)  # gets the roll pitch yaw in that order and then updates the yaw 
        self.yaw = euler_angles[2]
       

    def publish_data(self):
        """
        Publish `self.dist` and `self.yaw` on the `my_odom` topic.
        """
        # The `Point` object should be used simply as a data container for
        # `self.dist` and `self.yaw` so we can publish it on `my_odom`.
        point_msg = Point()
        point_msg.x = self.dist  
        point_msg.y = self.yaw   
        point_msg.z = 0.0       
        
        self.my_odom_pub.publish(point_msg)
        
        
if __name__ == '__main__':
    rospy.init_node('my_odom')
    MyOdom()
    rospy.spin()
