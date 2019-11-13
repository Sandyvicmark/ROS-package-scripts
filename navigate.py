#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
import math
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class subandpub():
	def __init__(self):
		self.naviListx = []
		self.naviListy = []
		num = int(raw_input('input the number of navi points: '))
		for i in range(num):
			self.naviListx.append(float(raw_input('input the x of point %d: ' % i)))
			self.naviListy.append(float(raw_input('input the y of point %d: ' % i)))
		rospy.init_node('naviPub','poseSub', anonymous=True)
		global naviPub
		naviPub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size = 10)
		rospy.Subscriber('/turtle1/pose', Pose, self.callback)
	
	def callback(self, msg):
		self.x = msg.x
		self.y = msg.y
		if not self.naviListx:
			rospy.loginfo('TRAVERSAL OF ALL NAVI POINTS COMPLETED!! Press ^C to exit!')
			while True:
				pass
		else:
			self.theta = msg.theta				#get current theta
			while self.theta < 0:				#make sure current theta is positive
				self.theta += 6.2832
			if self.theta > 3.1416:				#make current theta in [-180, +180]
				self.theta -= 6.2832
			if self.theta == 0:
				self.theta = 0.00001

			self.deltax = self.x - self.naviListx[0]
			if self.deltax == 0:
				self.deltax = 0.00001
			self.deltay = self.y - self.naviListy[0]
			self.dist = math.sqrt(self.deltax * self.deltax + self.deltay * self.deltay)
			if self.dist < 0.001 and self.naviListx:
				self.naviListx.remove(self.naviListx[0])
				self.naviListy.remove(self.naviListy[0])
			else: 
				self.destAng = math.atan(self.deltay/self.deltax)		#calculate desAng
				if self.deltax > 0:
					if self.destAng > 0:
						self.destAng -= 3.1416
					else:
						self.destAng += 3.1416
 
				self.angle = abs(self.theta - self.destAng)			#calculate angle
				self.vel_msg = Twist()
				if self.angle < 0.05:						#calculate linearspeed		
					self.vel_msg.linear.x = self.dist
					if self.vel_msg.linear.x > 2:
						self.vel_msg.linear.x = 2
					elif self.dist > 0.03 and self.vel_msg.linear.x < 0.5:
						self.vel_msg.linear.x = 0.5
				if self.angle > 0.02:						#calculate angularspeed
					if self.theta > 0 and self.destAng > 0:			#adjust the result according to different situation of theta and destAng
						if self.theta < self.destAng:
							self.vel_msg.angular.z = 2 * self.angle
							if self.vel_msg.angular.z > 3:
                                                       		self.vel_msg.angular.z = 3
						else:
							self.vel_msg.angular.z = -2 * self.angle
							if self.vel_msg.angular.z < -3:
	                                                        self.vel_msg.angular.z = -3
					elif self.theta < 0 and self.destAng < 0:
						if self.theta < self.destAng:
                                                        self.vel_msg.angular.z = 2 * self.angle
                                                        if self.vel_msg.angular.z > 3:
                                                                self.vel_msg.angular.z = 3
                                                else:
							self.vel_msg.angular.z = -2 * self.angle
                                                        if self.vel_msg.angular.z < -3:
                                                                self.vel_msg.angular.z = -3
					elif self.theta > 0 and self.destAng < 0:
						self.tmpAng = self.destAng + 3.1416
						if self.theta < self.tmpAng:
                                                        self.vel_msg.angular.z = -2 * abs(self.angle - 6.2832)
                                                        if self.vel_msg.angular.z < -3:
                                                                self.vel_msg.angular.z = -3
                                                else:
                                                        self.vel_msg.angular.z = 2 * abs(self.angle - 6.2832)
                                                        if self.vel_msg.angular.z > 3:
                                                                self.vel_msg.angular.z = 3
					elif self.theta < 0 and self.destAng > 0:
						self.tmpAng = self.destAng - 3.1416
						if self.theta < self.tmpAng:
                                                        self.vel_msg.angular.z = -2 * abs(self.angle - 6.2832)
                                                        if self.vel_msg.angular.z < -3:
                                                                self.vel_msg.angular.z = -3
                                                else:
                                                        self.vel_msg.angular.z = 2 * abs(self.angle - 6.2832)
                                                        if self.vel_msg.angular.z > 3:
                                                                self.vel_msg.angular.z = 3

				else:
					self.vel_msg.angular.z = 0

				self.pub(self.vel_msg)
				rospy.loginfo('dest: %.5f, theta: %.5f, angle: %.5f' % (self.destAng, self.theta, self.angle))
	
	def pub(self, msg):
		naviPub.publish(msg)

#def velPubInit(opjb):
#	rospy.init_node('follow_vel_pub','poseSub', anonymous=True)
#	follow_vel_pub = rospy.Publisher('objb/cmd_vel', Twist, queue_size = 10)

#obj1 = '/' + raw_input('Input the dest obj1: ')
#obj2 = '/' + raw_input('Input the dest obj2: ')
snp = subandpub()
rospy.spin()
#velPubInit(obj2)
