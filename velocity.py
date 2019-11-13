#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist

def velocity_pub():
	#INIT ROS NODE
	rospy.init_node('volocity_pub', anonymous = True)

	#CREATE A PUBLISHER, PUBLISH THE TOPIC OF /turtle1/cmd_vel, 
	#CLASS: geometry_msgs::Twist, LENGTH OF ARRAY: 10
	vel_pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size = 10)

	#SET RATE OF CIRCLE
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		#INIT THE CLASS OF MSG TO 'Twist'
		vel_msg = Twist()
		vel_msg.linear.x = 1.0
		vel_msg.angular.z = 0.5
		#PUBLISH MSG
		vel_pub.publish(vel_msg)
		rospy.loginfo('Published! [%.2f m/s, %.2f rad/s]' % (vel_msg.linear.x, vel_msg.angular.z))
		#SET INTERRUPT
		rate.sleep()

if __name__ == '__main__':
	try:
		velocity_pub()
	except rospy.ROSInterruptException:
		pass
