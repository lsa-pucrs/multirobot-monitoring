#!/usr/bin/env python

import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("I heard %s",data.data)
    print "total_errors = " + str(data.data)
    
def listener():
    rospy.init_node('node_name')
    rospy.Subscriber("total_errors", String, callback)
    print "total_errors = " + str(data.data)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
