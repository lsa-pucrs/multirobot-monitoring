#!/usr/bin/env python

import sys
sys.path.append("/opt/ros/hydro/lib/python2.7/dist-packages")

import os
os.environ['PATH'] = "/opt/ros/hydro/bin:" + os.environ['PATH']

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
STALE = 3
COUNT_sensors = 0

# TEMPLATE FOR READING PARAMETERS FROM COMMANDLINE
parser = OptionParser()
parser.add_option("-H", "--host", dest="host", default='localhost', help="Define the target host")
parser.add_option("-N", "--name", dest="name", default='all', help="Define the sensor name")
(options, args) = parser.parse_args()

# Set turtlebot ROS Master URI
os.environ['ROS_MASTER_URI'] = 'http://' + options.host  + ':11311'

total_level = None
OK_sensors = None
WARNING_sensors = None
CRITICAL_sensors = None
STALE_sensors = None


def callback_kobuki(data):
    global total_level
    global OK_sensors
    global WARNING_sensors
    global CRITICAL_sensors
    global STALE_sensors
    global COUNT_sensors

    ready = False

    while not ready:
        for current in data.status:
          from pprint import pprint
          if (options.name == "all" or options.name in current.name):

              # Calculate the total level
              if current.level >= total_level:
                total_level = current.level

              # Parse current.name string and keep only the part after the : 
              parse_name = current.name

              # Count how many sensors were found
              COUNT_sensors = COUNT_sensors + 1

              # Create CRITICAL sensors list
              if current.level == CRITICAL:
                  if CRITICAL_sensors != None:
                    CRITICAL_sensors = str(CRITICAL_sensors) + str(parse_name) + str(', ')
                  else:
                    CRITICAL_sensors = str(parse_name) + str(', ')

              # Create WARNING sensors list
              if current.level == WARNING:
                  if WARNING_sensors != None:
                    WARNING_sensors = str(WARNING_sensors) + str(parse_name) + str(', ')
                  else:
                    WARNING_sensors = str(parse_name) + str(', ')

              # Create OK sensors list
              if current.level == OK:
                  if OK_sensors != None:
                    OK_sensors = str(OK_sensors) + str(parse_name) + str(', ')
                  else:
                    OK_sensors = str(parse_name) + str(', ')       
              
              # Create STALE sensors list
              if current.level == STALE:
                  if STALE_sensors != None:
                    STALE_sensors = str(STALE_sensors) + str(parse_name) + str(', ')
                  else:
                    STALE_sensors = str(parse_name) + str(', ')       
        
        ready = True

    time = rospy.get_time()
    rospy.signal_shutdown(0)

def listener():
    rospy.init_node('ros_diagnostics', anonymous=True,  disable_signals=True)
    rospy.Subscriber("diagnostics_agg", DiagnosticArray , callback_kobuki)
    rospy.spin()

def myhook():

    description = None

    if STALE_sensors != None:
        if (description != None):
          description = str(description) + str("STAKE sensor(s) list: " + str(STALE_sensors))
        else:
          description = str("STALE sensor(s) list: " + str(STALE_sensors))

    if CRITICAL_sensors != None:
        if (description != None):
          description = str(description) + str("CRITICAL sensor(s) list: " + str(CRITICAL_sensors))
        else:
          description = "CRITICAL sensor(s) list: " + str(CRITICAL_sensors)

    if WARNING_sensors != None:
        if (description != None):
          description = str(description) + str("WARNING sensor(s) list: " + str(WARNING_sensors))
        else:
          description = str("WARNING sensor(s) list: " + str(WARNING_sensors))

    if OK_sensors != None:
        if (description != None):
          description = str(description) + str("OK sensor(s) list: " + str(OK_sensors))
        else:
          description = str("OK sensor(s) list: " + str(OK_sensors))

    # Remove last comma
    if description != None:
      description = description[:-2]

    if COUNT_sensors == 0:
      print "CRITICAL - %s" % (description)
      exiting(CRITICAL)
    if total_level >= CRITICAL:
      print "CRITICAL - %s" % (description)
      exiting(CRITICAL)
    elif total_level == WARNING:
      print "WARNING - %s" % (description)
      exiting(WARNING)
    else:
      print "OK - %s" % (description)
      exiting(OK)

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
        if len(sys.argv) < 1:
            print "usage %s -N <name of sensor>" % (sys.argv[0])
	    exiting(UNKNOWN)
        rospy.on_shutdown(myhook)
        listener()
    except rospy.ROSInterruptException:
        exit
