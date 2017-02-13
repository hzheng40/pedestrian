#!/usr/bin/env python

from __future__ import print_function
import rospy
import cv2
from imutils.object_detection import non_max_suppression
from imutils import paths
# import faster_nms
import imutils
import sys
import numpy as np
from sensor_msgs.msg import Image
# from std_msgs.msg import String
# from std_msgs.msg import Float64MultiArray
# from std_msgs.msg import Header
# from geometry_msgs.msg import Pose, PoseArray
from cv_bridge import CvBridge, CvBridgeError

# Malisiewicz et al.
def non_max_suppression_fast(boxes, overlapThresh):
	# if there are no boxes, return an empty list
	if len(boxes) == 0:
		return []
 
	# if the bounding boxes integers, convert them to floats --
	# this is important since we'll be doing a bunch of divisions
	if boxes.dtype.kind == "i":
		boxes = boxes.astype("float")
 
	# initialize the list of picked indexes	
	pick = []
 
	# grab the coordinates of the bounding boxes
	x1 = boxes[:,0]
	y1 = boxes[:,1]
	x2 = boxes[:,2]
	y2 = boxes[:,3]
 
	# compute the area of the bounding boxes and sort the bounding
	# boxes by the bottom-right y-coordinate of the bounding box
	area = (x2 - x1 + 1) * (y2 - y1 + 1)
	idxs = np.argsort(y2)
 
	# keep looping while some indexes still remain in the indexes
	# list
	while len(idxs) > 0:
		# grab the last index in the indexes list and add the
		# index value to the list of picked indexes
		last = len(idxs) - 1
		i = idxs[last]
		pick.append(i)
 
		# find the largest (x, y) coordinates for the start of
		# the bounding box and the smallest (x, y) coordinates
		# for the end of the bounding box
		xx1 = np.maximum(x1[i], x1[idxs[:last]])
		yy1 = np.maximum(y1[i], y1[idxs[:last]])
		xx2 = np.minimum(x2[i], x2[idxs[:last]])
		yy2 = np.minimum(y2[i], y2[idxs[:last]])
 
		# compute the width and height of the bounding box
		w = np.maximum(0, xx2 - xx1 + 1)
		h = np.maximum(0, yy2 - yy1 + 1)
 
		# compute the ratio of overlap
		overlap = (w * h) / area[idxs[:last]]
 
		# delete all indexes from the index list that have
		idxs = np.delete(idxs, np.concatenate(([last],
			np.where(overlap > overlapThresh)[0])))
 
	# return only the bounding boxes that were picked using the
	# integer data type
	return boxes[pick].astype("int")

class image_converter:
	def __init__(self):
		# subscribers, bridge and publisher init
		self.image_sub = rospy.Subscriber('/camera/rgb/image_color', Image, self.callback)
		self.bridge = CvBridge()
		self.image_pub = rospy.Publisher('results', Image, queue_size=10)
		# self.coord_pub = rospy.Publisher('coordinates', PoseArray, queue_size=10)
		# self.coordinates = PoseArray()

		# using hog descriptor to detect human
		self.HOG = cv2.HOGDescriptor()
		self.HOG.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

		# using haar cascade to detect human
		# self.cascade = cv2.CascadeClassifier('haarcascade_pedestrian.xml')

	def callback(self, data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, 'bgr8')
		except CvBridgeError as e:
			print(e)

		# for haar cascade
		# TODO: finish detection with haar cascade
		# cv_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		# self.cascade.detectMultiScale(cv_gray)

		# for hog descriptor
		# TODO: try different scales to find improved speed
		cv_image = imutils.resize(cv_image, width=min(250, cv_image.shape[1]))
		(rects, weights) = self.HOG.detectMultiScale(cv_image, winStride=(4,4), padding=(8,8), scale=1.05)
		rects = np.array([[x,y,x+w,y+h] for (x,y,w,h) in rects])

		# non max suppression
		# TODO test this faster nms out
		pick = non_max_suppression_fast(rects, overlapThresh=0.65)
		for(xA, yA, xB, yB) in pick:
			cv2.rectangle(cv_image, (xA,yA), (xB, yB), (0,255,0), 2)
		
		# TODO: publish the coordinates
		# if using PoseArray, length must be multiple of 4, each group is a rect
		# self.coord_pub.publish(pick)
		



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
