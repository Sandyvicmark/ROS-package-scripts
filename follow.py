#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class subandpub():
	def __init__(self):
		rospy.init_node('follow_vel_pub','poseSub', anonymous=True)
		global follow_vel_pub
		follow_vel_pub = rospy.Publisher('turtle2/cmd_vel', Twist, queue_size = 10)
		rospy.Subscriber('/turtle1/pose', Pose, self.callbacka)
        	rospy.Subscriber('/turtle2/pose', Pose, self.callbackb)
	
	def callbacka(self, msg):
		self.xa = msg.x
		self.ya = msg.y	

	def callbackb(self, msg):
		self.xb = msg.x
		self.yb = msg.y
		if msg.theta < 0:
			self.thetab = msg.theta + 6.2832
		else:
			self.thetab = msg.theta
		self.deltax = self.xb - self.xa
		if self.deltax == 0:
			self.deltax = 0.00001
		self.deltay = self.yb - self.ya
		self.dist = math.sqrt(self.deltax * self.deltax + self.deltay * self.deltay)
		if self.deltax > 0:
			self.destAng = math.atan(self.deltay/self.deltax) + 3.1416
		elif self.deltax < 0:
			self.destAng = math.atan(self.deltay/self.deltax)
		if self.destAng < 0:
			self.destAng += 6.2832
		self.tmpAng = self.destAng + 3.1416
		self.angle = abs(self.thetab - self.destAng)
		self.vel_msg = Twist()
		if self.dist > 1.2:
			self.vel_msg.linear.x = self.dist
#			if self.vel_msg.linear.x > 3:
#				self.vel_msg.linear.x = 3
		elif self.dist < 1:
			self.vel_msg.linear.x = -2.5 * self.dist
		if self.angle > 0.08:
			if self.destAng > 3.1416 and self.thetab > self.destAng:
				pass
			elif self.destAng < 3.1416 and self.thetab < self.destAng:
				self.tmpAng -= 6.2832
			else:			
				if self.tmpAng > 6.2832:
					self.tmpAng -= 6.2832
			if self.tmpAng > self.thetab:
				self.vel_msg.angular.z = -1.5 * self.angle
			else:
				self.vel_msg.angular.z = 1.5 * self.angle
		else:
			self.vel_msg.angular.z = 0

		self.pub(self.vel_msg)
		rospy.loginfo('theta: %.3f, dest: %.3f, angle: %.3f'%(self.thetab*180/3.14, self.destAng*180/3.14, self.angle*180/3.14))
	def pub(self, msg):
		follow_vel_pub.publish(msg)

#def velPubInit(opjb):
#	rospy.init_node('follow_vel_pub','poseSub', anonymous=True)
#	follow_vel_pub = rospy.Publisher('objb/cmd_vel', Twist, queue_size = 10)

#obj1 = '/' + raw_input('Input the dest obj1: ')
#obj2 = '/' + raw_input('Input the dest obj2: ')
snp = subandpub()
rospy.spin()
#velPubInit(obj2)
