#!/usr/bin/env python

# collecting data from turtlebot (image, human input)
# frame and corresponding instruction.

from __future__ import print_function
import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty
import subprocess
import rosbag
from sensor_msgs.msg import Image

class data_collectors:
	def __init__(self):
		self.image_sub = rospy.Subscriber('/camera/rgb/image_color', Image, self.callback)
		self.msg="""
				Control Your Turtlebot!
				---------------------------
				Moving around:
				   u    i    o
				   j    k    l
				   m    ,    .
				q/z : increase/decrease max speeds by 10%
				w/x : increase/decrease only linear speed by 10%
				e/c : increase/decrease only angular speed by 10%
				space key, k : force stop
				anything else : stop smoothly
				CTRL-C to quit
				"""
		self.moveBindings = {
							'i':(1,0),
							'o':(1,-1),
							'j':(0,1),
							'l':(0,-1),
							'u':(1,1),
							',':(-1,0),
							'.':(-1,1),
							'm':(-1-1)
							}
		self.speedBindings={
							'q':(1.1,1.1),
							'z':(.9,.9),
							'w':(1.1,1),
							'x':(.9,1),
							'e':(1,1.1),
							'c':(1,0.9)
							}
		self.bag = rosbag.Bag('test.bag', 'w')
		self.speed = .2
		self.turn = 1

	def getKey():
		tty.setraw(sys.stdin.fileno())
		rlist,_, _ = select.select([sys.stdin],[],[],0.1)
		if rlist:
			key=sys.stdin.read(1)
		else:
			key=''
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
		return key

	def vels(speed, turn):
		return "currently:\tspeed %s\tturn %s " % (self.speed, self.turn)

	def callback(self, data):
		self.bag.write('image', data)
		self.bag.write('instruction', self.getKey())


def main(args):
	dc = data_collectors()
	settings = termios.tcsetattr(sys.stdin)
	rospy.init_node('turtlebot_data_collect', anonymous=True)
	pub = rospy.Publisher('~cmd_vel', Twits, queue_size=5)
	x = 0
    th = 0
    status = 0
    count = 0
    acc = 0.1
    target_speed = 0
    target_turn = 0
    control_speed = 0
    control_turn = 0
    try:
        print msg
        print vels(speed,turn)
        while(1):
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
                count = 0
            elif key in speedBindings.keys():
                speed = speed * speedBindings[key][0]
                turn = turn * speedBindings[key][1]
                count = 0

                print vels(speed,turn)
                if (status == 14):
                    print msg
                status = (status + 1) % 15
            elif key == ' ' or key == 'k' :
                x = 0
                th = 0
                control_speed = 0
                control_turn = 0
            else:
                count = count + 1
                if count > 4:
                    x = 0
                    th = 0
                if (key == '\x03'):
                    break

            target_speed = speed * x
            target_turn = turn * th

            if target_speed > control_speed:
                control_speed = min( target_speed, control_speed + 0.02 )
            elif target_speed < control_speed:
                control_speed = max( target_speed, control_speed - 0.02 )
            else:
                control_speed = target_speed

            if target_turn > control_turn:
                control_turn = min( target_turn, control_turn + 0.1 )
            elif target_turn < control_turn:
                control_turn = max( target_turn, control_turn - 0.1 )
            else:
                control_turn = target_turn

            twist = Twist()
            twist.linear.x = control_speed; twist.linear.y = 0; twist.linear.z = 0
            twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = control_turn
            pub.publish(twist)

            #print("loop: {0}".format(count))
            #print("target: vx: {0}, wz: {1}".format(target_speed, target_turn))
            #print("publihsed: vx: {0}, wz: {1}".format(twist.linear.x, twist.angular.z))

    except:
        print e

    finally:
        twist = Twist()
        twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
        pub.publish(twist)

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    self.bag.close()


if __name__ == '__main__':
	main(sys.argv)