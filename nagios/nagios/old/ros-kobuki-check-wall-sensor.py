#!/usr/bin/env python

import sys
sys.path.append("/home/schreiner/catkin_ws_hydro/install/lib/python2.7/dist-packages")
sys.path.append("/opt/ros/hydro/lib/python2.7/dist-packages")

import os
os.environ['PATH'] = "/opt/ros/hydro/bin:" + os.environ['PATH']
os.environ['ROS_PACKAGE_PATH']= '/home/schreiner/catkin_ws_hydro/install/share:/home/schreiner/catkin_ws_hydro/install/stacks:/opt/ros/hydro/share:/opt/ros/hydro/stacks'

from optparse import OptionParser

import rospy
import rosnode
import os
import roslib
import sys
roslib.load_manifest('linux_hardware')
from linux_hardware.msg import LaptopChargeStatus
from diagnostic_msgs.msg import DiagnosticStatus, DiagnosticArray, KeyValue

# Exit statuses recognized by Nagios
UNKNOWN = -1
OK = 0
WARNING = 1
CRITICAL = 2

# TEMPLATE FOR READING PARAMETERS FROM COMMANDLINE
parser = OptionParser()
parser.add_option("-H", "--host", dest="host", default='localhost', help="A message to print after OK - ")
parser.add_option("-w", "--warning", dest="warning", default='40', help="A message to print after OK - ")
parser.add_option("-c", "--critical", dest="critical", default='20', help="A message to print after OK - ")
(options, args) = parser.parse_args()

# Set turtlebot ROS Master URI
os.environ['ROS_MASTER_URI'] = 'http://' + options.host  + ':11311'

kobuki_value = None

def callback_kobuki(data):
    global kobuki_value

    ready = False

    while not ready:
        for current in data.status:
            #print current.name
            if current.name == "mobile_base_nodelet_manager: Wall Sensor":
                #print current.name
                #from pprint import pprint
                #pprint(current.message)
                kobuki_value = current.message
                ready = True

    time = rospy.get_time()
    # kobuki_percentage = int(float(kobuki_percentage))
    rospy.signal_shutdown(0)

def listener():
    rospy.init_node('check_battery_kobuki', anonymous=True,  disable_signals=True)
    rospy.Subscriber("diagnostics", DiagnosticArray , callback_kobuki)
    rospy.spin()

def myhook():
    if kobuki_value == 'All right':
        print "OK - Kobuki Wall Sensor All right"
        exiting(OK)
    else:
        print "CRITICAL - Kobuki Wall Sensor Error"
        exiting(CRITICAL)

def exiting(value):
    try:
	sys.stdout.flush()
	os._exit(value)
    except:
        pass

if __name__ == '__main__':
    try:
        master = rospy.get_master()
        master.getPid()
    except Exception:
        print "UNKNOWN - Roscore not available"
	exiting(UNKNOWN)

    try:
        if len(sys.argv) < 5:
            print "usage %s -c <critical> -w <warning>" % (sys.argv[0])
	    exiting(UNKNOWN)
        rospy.on_shutdown(myhook)
        listener()
    except rospy.ROSInterruptException:
        exit