import rospy, rosbag
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
import subprocess
import h5py

# input is a 227 x 227 rgb
subprocess.call(['./run_bag.sh'])

bag = rosbag.Bag('./turtle.bag')

# t1 ms1 tm1 -> image
# t2 ms2 tm2 -> instruction
# t2 ms2 tm2 -> image

topic_buffer = None
msg_buffer = None



for topic, msg, t in bag.read_messages(topics=['/camera/rgb/image_color', 'instructions']):
	if topic == topic_buffer:
		