import rospy, rosbag
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
import subprocess
import h5py

# input is a 227 x 227 rgb
subprocess.call(['./run_bag.sh'])