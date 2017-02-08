#!/usr/bin/env python

from __future__ import print_function
import rospy
import cv2
from imutils.object_detection import non_max_suppression
from imutils import paths
import imutils
import sys
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

class image_converter:
	def __init__(self):
		# subscribers, bridge and publisher init
		self.image_sub = rospy.Subscriber('/camera/rgb/image_color', Image, self.callback)
		self.bridge = CvBridge()
		self.image_pub = rospy.Publisher('results', Image, queue_size=10)

		# using hog descriptor to detect human
		self.HOG = cv2.HOGDescriptor()
		self.HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

		# using haar cascade to detect human
		self.cascade = cv2.CascadeClassifier('haarcascade_pedestrian.xml')

	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
		except CvBridgeError as e:
			print(e)

		# for haar cascade
		# TODO: finish detection with haar cascade
		cv_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		self.cascade.detectMultiScale(cv_gray)

		# for hog descriptor
		# TODO: try different scales to find improved speed
		cv_image = imutils.resize(cv_image, width=min(400, cv_image.shape[1]))
		(rects, weights) = self.HOG.detectMultiScale(cv_image, winStride=(4,4), padding=(8,8), scale=1.05)
		rects = np.array([[x,y,x+w,y+h] for (x,y,w,h) in rects])

		# non max suppression
		pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
		for(xA, yA, xB, yB) in pick:
			cv2.rectangle(cv_image, (xA,yA), (xB, yB), (0,255,0), 2)

		#cv2.imshow("Before NMS", orig)
		#cv2.imshow('After NMS', cv_image)
		#cv2.waitKey(0)
		self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, 'bgr8'))


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
