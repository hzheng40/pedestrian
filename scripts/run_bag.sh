# !/bin/bash

roslaunch freenect_launch freenect.launch
roslaunch turtlebot_bringup minimal.launch
roslaunch runbag.launch

rosbag record /camera/rgb/image_color /instructions
