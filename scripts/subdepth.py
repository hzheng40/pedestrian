#!/usr/bin/env python

import rospy
import sys
from sensor_msgs.msg import PointCloud
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray


class depth_finder:
	def __init__(self):
		# init
		# TODO: find the topic name to subscribe
		self.depth_sub = rospy.Subscriber('/camera/depth/', PointCloud, self.depthcallback)
		self.coord_sub = rospy.Subscriber('coordinates', Float64MultiArray, self.callback)
		self.depth_pub = rospy.Publisher('depth', Float64, queue_size=10)
		self.coordinates = []
		self.depth = None

	def depthcallback(self, data):
		# TODO: find the mapping between camera and IR sensor



	def callback(self, data):
		# TODO: find the depth for the pedestrian found


def main(args):
	df = depth_finder()
	rospy.init_node('depth_finder', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print('Shutting down.')

if __name__ == '__main__':
	main(sys.argv)