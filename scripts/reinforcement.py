#!/usr/bin/env python


from future import print_function
import rospy
import sys
import numpy as np 
from sensor_msgs.msg import Image, LaserScan
from std_msgs.msg import String, Float64MultiArray, Header
from geometry_msgs.msg import Pose, PoseArray, Point, Twist
from nav_msgs.msg import OccupancyGrid, MapMetaData

class Directions:
	STOP = 'Stop'
	LEFT = 'Left'
	RIGHT = 'Right'
	FORWARD = 'Forward'
	


class Configuration:
	def __init__(self):
		self.pos = None
		self.direction = None
		self.command_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

	def getPosition(self):
		return self.pos

	def getDirection(self):
		return self.direction

	def move(self, command):
		# command should be in Twist
		self.command_pub.publish(command)

	def generateSuccessor(self, vector):
		x, y = self.pos
		dx, dy = vector



class Grid:
	def __init__(self):
		self.


class reinforcement:
	def __init__(self):
		self.grids = []
		self.policies = []
		self.coord_pub = rospy.Subscriber('coord', PoseArray, coord_callback)
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

