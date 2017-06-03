#!/usr/bin/env python

# reading the bagfiles

import rosbag
from std_msgs.msg import String
from sensor_msgs.msg import Image
import subprocess


# using shell script to prep???
subprocess.call([' ./prep.sh'])


bag = rosbag.Bag('test.bag')
for topic, msg, t in bag.read_messages(topics=['instruction','image'])
	# reminder 6 classifications/directions
	# u  i  o
	# j  k  l

	if 