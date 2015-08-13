#!/usr/bin/env python

import rospy
from std_msgs.msg import String

########################################################################
# Simulation config
total_errors = 2
total_warnings = 0


pub = rospy.Publisher('total_errors', String, queue_size=10)
#pub2 = rospy.Publisher('total_warnings', String, queue_size=10)
rospy.init_node('node_name')
r = rospy.Rate(10) # 10hz
while not rospy.is_shutdown():
   pub.publish(str(total_errors))
#   pub2.publish(str(total_warnings))
   r.sleep()
