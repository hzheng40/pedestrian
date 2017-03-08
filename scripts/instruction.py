#!/usr/bin/env python

# instruction from reinforcement learning to turtlebot
# Author: Hongrui Zheng
# 3/8/2017

from __future__ import print_function
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from reinforcement import Directions


class Instruction:
	def __init__(self):
		#subscribing from the reinforcement results node
		self.instruction_sub = rospy.Subscriber('instruction', String, self.instruction_callback)
		#publishing to the turtlebot velocity
		self.instruction_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)



	def instruction_callback(self, data):
		# cases: stopping, turning left, turning right, forward, left 45, right 45
		if data == Directions.STOP:
			self.publish_vel(0.0, 0.0)
		else if data == Directions.LEFT:
			self.publish_vel(5.0, 0.0)
		else if data == Directions.Right:
			self.publish_vel(-5.0, 0.0)
		else if data == Directions.FORWARD:
			self.publish_vel(0.0, 5.0)
		else if data == Directions.FORWARDL:
			self.publish_vel(5.0, 5.0)
		else if data == Directions.ForwardR:
			self.publish_vel(-5.0, 5.0)
		else:
			self.publish_vel(0.0, 0.0)


	def publish_vel(self, _angular, _linear):
		vel = Twist()
		vel.angular.z = _angular
		vel.linear.x = _linear
		self.instruction_pub.publish(vel)