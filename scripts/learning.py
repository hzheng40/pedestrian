#!/usr/bin/env python

from __future__ import print_function
import tensorflow as tf
import numpy as np
import rospy, rosbag, sys, os, shutil
from std_msgs.msg import Image
from os import listdir, mkdir
from shutil import copyfile
from os.path import isfile, join



