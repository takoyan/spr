#!/usr/bin/env python
#encoding: utf-8

import rospy
from std_msgs.msg import String

rospy.init_node('tester', anonymous=True)
pub = rospy.Publisher('spr_state', String, queue_size=10)
rate = rospy.Rate(10)

while not rospy.is_shutdown():
	spr_t = String()
	spr_t.data = "test"
	pub.publish(spr_t)
        print('publish')
	rate.sleep()
