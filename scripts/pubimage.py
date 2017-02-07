#!/usr/bin/env python
from __future__ import print_function
import rospy
import sys
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

   
def publish_image(img_pub, img_name):
	img = cv2.imread(img_name)
	try:
		msg_img = CvBridge().cv2_to_imgmsg(img)
	except CvBridgeError as e:
		print(e)
	try:
		img_pub.publish(msg_img, 'bgr8')
	except CvBridgeError as e:
		print(e)

def main(args):
	rospy.init_node('image_publisher', anonymous=True)
	image_pub = rospy.Publisher('image_pub', Image, queue_size=10)
	img_name = 'pedtest.jpg'

	publish_image(image_pub, img_name)


if __name__ == '__main__':
	main(sys.argv)