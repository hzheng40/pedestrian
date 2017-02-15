import rospy
import sys
import sys
import numpy as np 
from sensor_msgs.msg import Image
from std_msgs.msg import String, Float64MultiArray, Header
from geometry_msgs.msg import Pose, PoseArray, Point

# 



class reinforcement:
	def __init__(self):
		self.grids = []
		self.policies = []
		self.coord_pub = rospy.Subscriber('coord', PoseArray, coord_callback)
		self.action_pub = rospy.Publisher('action', )
		self.alpha = 0.1
		self.decision = None
		self.coord = Point()
		self.legalActions = dict()

		allD = ['F','B','L','R']
		noF = ['B','L','R']
		noB = ['F','L','R']
		noL = ['F','B','R']
		noR = ['F','B','L']
		FB = ['F','B']
		LR = ['L','R']
		F = ['F']
		B = ['B']
		L = ['L']
		R = ['R']

		self.legalActions = {1: }

	def publishPolicy(self):
		self.action_pub.publish(self.decision)


	def coord_callback(self, data):
		


	def getLegalAction(self, state):
		return self.legalActions[state]

