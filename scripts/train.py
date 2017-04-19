#!/usr/bin/env python

# training a image classification network

from __future__ import print_function
import rospy
from geometry_msgs.msg import Twist
import rosbag
from sensor_msgs.msg import Image
import tensorflow as tf
import numpy as np
import os
import cv2

# first unpack the rosbag to get the images and classification

# create the directories for training images
classifications = ['u','i','o','j','k','l']
for cl in classifications:
	os.mkdir('./'+cl)

# unpack and save images to their corresponding directories
sequence_no = 0
bag = rosbag.Bag('test.bag')
for topic, msg, t in bag.read_messages(topics=['chatter', 'numbers']):
	print msg #DEBUG
	# put images in corresponding directories
	if msg.instruction == 'u':
		cv2.imwrite('image_'+str(sequence_no)+'.jpg', msg.image)
		os.rename('./'+'image_'+str(sequence_no)+'.jpg', './u')
	else if msg.instruction == 'i':

	else if msg.instruction == 'o':

	else if msg.instruction == 'j':

	else if msg.instruction == 'k':

	else if msg.instruction == 'l':

	sequence_no = sequence_no + 1