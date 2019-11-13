#!/usr/bin/env python
# -*- coding = UTF-8 -*-

import rospy
from turtlesim.msg import Pose

def callback1(msg):
	rospy.loginfo('Position: x: %.3f, y: %.3f\nAngle: %.3f' % (msg.x, msg.y, msg.theta))
	
def callback2(msg):
	rospy.loginfo('Position: x: %.3f, y: %.3f' % (msg.x, msg.y))

def poseSubscriber(obj):
	rospy.init_node('poseSub', anonymous = True)
	rospy.Subscriber(obj + '/pose', Pose, callback1)
	rospy.Subscriber('/turtle2/pose', Pose, callback2)
	rospy.spin()

obj = '/' + raw_input('Input the dest obj: ')
poseSubscriber(obj)
