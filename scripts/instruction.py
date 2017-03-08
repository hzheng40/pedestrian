#!/usr/bin/env python

# instruction from reinforcement learning to turtlebot
# Author: Hongrui Zheng
# 3/8/2017

from __future__ import print_function
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class 

class Instruction:
	def __init__(self):
		#subscribing from the reinforcement results node
		self.instruction_sub = rospy.Subscriber('instruction', String, self.instruction_callback)
		#publishing to the turtlebot velocity
		self.instruction_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)



	def instruction_callback(self, data):
		# cases: stopping, turning left, turning right, forward, left 45, right 45
		if cases
 