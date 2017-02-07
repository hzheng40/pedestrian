#!/usr/bin/env python

from __future__ import print_function
import rospy
import cv2
import sys
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

class image_converter:
	def __init__(self):
		self.image_sub = rospy.Subscriber('/camera/rgb/image_color', Image, self.callback)
		self.bridge = CvBridge()
		self.flag_pub = rospy.Publisher('flag', String, queue_size=10)

	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
		except CvBridgeError as e:
			print(e)
		self.flag_pub.publish('hello')
		cv2.imshow("image window", cv_image)
		cv2.waitKey(0)


def main(args):
	ic = image_converter()
	rospy.init_node('image_converter', anonymous=True)
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print('shutting down')
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
