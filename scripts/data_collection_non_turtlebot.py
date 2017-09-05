#!/usr/bin/env python

# collecting training data from non-turtlebot vehicle

from __future__ import print_function
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image

class data_collectors:
	def __init__(self):
		self.image_sub = rospy.Subscriber('')