#!/usr/bin/env python3
import math
import rospy
from geometry_msgs.msg import Point, Pose, Twist
from tf.transformations import euler_from_quaternion

# BasicMover
class BasicMover:
    def __init__(self):
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.twist = Twist()

        self.my_odom_sub = rospy.Subscriber('my_odom', Point, self.my_odom_cb)
        self.cur_yaw = None
        self.cur_dist = 0.0
        while self.cur_yaw is None:
            pass
        # print("exit now")
        # Current heading of the robot.

    def my_odom_cb(self, msg):
        """Callback function for `self.my_odom_sub`."""
        print(f"cur dist :{msg.x}")
        self.cur_dist = msg.x  
        self.cur_yaw = msg.y

  
    def normalize_angle(self, angle):
       
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle
        # makes it so that any angle u give it it will be in the range of pi,-pi


    def turn_to_heading(self, target_yaw):
        """
        Turns the robot to the heading `target_yaw`.
        """
        
        self.twist = Twist()
        
        rate = rospy.Rate(10) 
        actual_yaw = target_yaw + self.cur_yaw
        while not rospy.is_shutdown():
            yaw_delta = self.normalize_angle(actual_yaw - self.cur_yaw)
            if abs(yaw_delta) <= 0.0006:  
                break
            # print("cur yaw:",self.cur_yaw)
            if yaw_delta > 0:  # turn left
                if yaw_delta <0.1:
                    angular_velocity = 0.035
                elif yaw_delta < 0.005:
                    angular_velocity = 0.00345
                else:
                    angular_velocity = 1.0

            else:# turn right
                if yaw_delta >-0.2:
                    angular_velocity = -0.035
                elif yaw_delta > -0.005:
                    angular_velocity = -0.00345
                else:
                    angular_velocity = -1.0
                
            self.twist.angular.z = angular_velocity
            self.cmd_vel_pub.publish(self.twist)
            rate.sleep()

        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)



    def move_forward(self, target_dist):
        """Moves the robot forward by `target_dist`."""
        
        self.twist = Twist()
        
        rate = rospy.Rate(10) #basiclaly that it sends info 10times a second

        actual_dist = self.cur_dist + target_dist
        # print("curDist:",self.cur_dist)
        # print("actualDist:",actual_dist)
        while not (self.cur_dist <= actual_dist +.01 and self.cur_dist >= actual_dist-.01):
            print(self.cur_dist)
            # error = abs(actual_dist-self.cur_dist)
            # print(f"error: {error}")
            self.twist.linear.x = 0.1
            if actual_dist-self.cur_dist <0.05:
                self.twist.linear.x = 0.01
            # print (self.twist.linear.x)
            
            self.cmd_vel_pub.publish(self.twist)
            rate.sleep()
        self.twist.linear.x = 0.0
        self.cmd_vel_pub.publish(self.twist)
        
  
    def out_and_back(self, target_dist):
        """
        This function:
        1. moves the robot forward by `target_dist`;
        2. turns the robot by 180 degrees; and
        3. moves the robot forward by `target_dist`.
        """
        BasicMover.move_forward(self, target_dist)
        BasicMover().turn_to_heading(math.pi)
        BasicMover.move_forward(self, target_dist)

    def draw_square(self, side_length):
        """
        This function moves the robot in a square with `side_length` meter sides.
        """ 
        # for i in range(2):  
        #     self.move_forward(side_length)
        #     self.turn_to_heading(((i + 1) * (math.pi / 2)))
        # self.move_forward(side_length)
        # self.turn_to_heading(3* (math.pi / 2)+.06)
        # self.move_forward(side_length)
        # self.turn_to_heading(2* (math.pi))
        for i in range (4):
            self.move_forward(side_length)
            self.turn_to_heading(math.pi/2)
              
    def move_in_a_circle(self, r):
        """Moves the robot in a circle with radius `r`"""
        self.twist = Twist()

         
        linear_velocity = 0.2  
        finish_dist = self.cur_dist + 2*r*math.pi
        # w = v / r
        angular_velocity = linear_velocity / r  

        rate = rospy.Rate(10)  # 10 Hz loop

        while not rospy.is_shutdown():
            self.twist.linear.x = linear_velocity
            self.twist.angular.z = angular_velocity
            self.cmd_vel_pub.publish(self.twist)
            rate.sleep()
            if (self.cur_dist > finish_dist):
                break  
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self.cmd_vel_pub.publish(self.twist)

        
    def rotate_in_place(self):
        """For debugging."""
        twist = Twist()
        
        rate = rospy.Rate(10)

        while not rospy.is_shutdown():
            twist.angular.z = 0.1
            self.cmd_vel_pub.publish(twist)
            rate.sleep()
    # def run(self):
    #     self.twist = Twist()
        
    #     rate = rospy.Rate(10) #basiclaly that it runs 10times a second
    #     counter = 0

    #     while not rospy.is_shutdown():
    #         counter += 0.1
            
    #     #   first half
    #         if counter<30:
    #             self.twist.linear.x = counter / 30 #it will reach max speed of 1 when at 30 seconds
    #         # second half
    #         elif counter>30 and counter <= 60: #start to decelerate after 30 seconds until it reaches speed 0
    #             self.twist.linear.x = -(1-((counter-30)/ 30))
    #         # done
            
    #         print (self.twist.linear.x )
    #         print (counter)
    #         self.cmd_vel_pub.publish(self.twist)
    #         rate.sleep()


if __name__ == '__main__':
    rospy.init_node('basic_mover')
    

    BasicMover().out_and_back(1)
    # BasicMover().draw_square(1)
    # BasicMover().move_in_a_circle(1)
    # BasicMover().rotate_in_place()
    # BasicMover().move_forward(1)
 
    rospy.signal_shutdown("finished")

