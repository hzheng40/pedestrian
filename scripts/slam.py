#!/usr/bin/env python

# gmapping subscribes to tf and scan, publishes to map_metadata, map, ~entropy

import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float64
from nav_msgs.msg import MapMetaData, OccupancyGrid#!/usr/bin/env python


class slam:
	def __init__(self):
		self.map_pub = rospy.Publisher('map', OccupancyGrid, queue_size=10)
		self.




	def 