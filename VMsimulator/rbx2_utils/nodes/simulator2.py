#!/usr/bin/env python

import roslib; # roslib.load_manifest('pr2_motors_analyzer')

import rospy, random, md5
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

def motor():
        # Build the diagnostics array message
        msg = DiagnosticArray()
        msg.header.stamp = rospy.Time.now()
        for cont in range(1,6):
	    status = DiagnosticStatus()
	    status.name = "Motor " + str(cont)
	    status.hardware_id = md5.new(str(status.name)).hexdigest()
	    random.seed()
	    level = random.randint(0, 100)
	    #print level
	    if level < 95:
		status.message = 'Running'
		status.level = DiagnosticStatus.OK
	    elif level < 99:
		status.message = 'Warning'
		status.level = DiagnosticStatus.WARN
	    else:
		status.message = 'Stopped'
		status.level = DiagnosticStatus.ERROR
	    msg.status.append(status)
	return msg

def camera():
        # Build the diagnostics array message
        msg = DiagnosticArray()
        msg.header.stamp = rospy.Time.now()
        for cont in range(1,2):
	    status = DiagnosticStatus()
	    status.name = "Cam " + str(cont)
	    status.hardware_id = md5.new(str(status.name)).hexdigest()
	    random.seed()
	    level = random.randint(0, 100)
	    #print level
	    if level < 95:
		status.message = 'OK'
		status.level = DiagnosticStatus.OK
	    elif level < 99:
		status.message = 'Warning'
		status.level = DiagnosticStatus.WARN
	    else:
		status.message = 'Error'
		status.level = DiagnosticStatus.ERROR

	    msg.status.append(status)
		    
	return msg


def temperature():
        # Build the diagnostics array message
        msg = DiagnosticArray()
        msg.header.stamp = rospy.Time.now()
        for cont in range(1,3):
	    status = DiagnosticStatus()
	    status.name = "Sensor " + str(cont)
	    status.hardware_id = md5.new(str(status.name)).hexdigest()
	    random.seed()
	    level = random.randint(0, 100)
	    #print level
	    if level < 95:
                temp = random.randint(15, 50)
		status.message = str(temp) + ' degrees'
		status.level = DiagnosticStatus.OK
	    elif level < 99:
                temp = random.randint(51, 80)
		status.message = str(temp) + ' degrees'
		status.level = DiagnosticStatus.WARN
	    else:
                temp = random.randint(80, 99)
		status.message = str(temp) + ' degrees'
		status.level = DiagnosticStatus.ERROR

	    msg.status.append(status)
		    
	return msg

def laser():
        # Build the diagnostics array message
        msg = DiagnosticArray()
        msg.header.stamp = rospy.Time.now()
        for cont in range(1,3):
	    status = DiagnosticStatus()
	    status.name = "Laser " + str(cont)
	    status.hardware_id = md5.new(str(status.name)).hexdigest()
	    random.seed()
	    level = random.randint(0, 100)
	    #print level
	    if level < 95:
		status.message = 'Normal'
		status.level = DiagnosticStatus.OK
	    elif level < 99:
		status.message = 'Warning'
		status.level = DiagnosticStatus.WARN
	    else:
		status.message = 'Error'
		status.level = DiagnosticStatus.ERROR

	    msg.status.append(status)
		    
	return msg


def battery():
            # Initialize the diagnostics status
            status = DiagnosticStatus()
            status.name = "Robot Battery"

	    current_battery_level = random.randint(1, 100)

	    if current_battery_level < error_battery_level:
		status.message = "Low " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.ERROR
	    elif current_battery_level < warn_battery_level:
		status.message = "Warning " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.WARN     
	    else:
		status.message = "OK " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.OK
            
            # Add the raw battery level to the diagnostics message
            status.values.append(KeyValue("Level", str(current_battery_level)))
            
            # Build the diagnostics array message
            msg = DiagnosticArray()
            msg.header.stamp = rospy.Time.now()
            msg.status.append(status)

            return msg

def laptop_battery():
            # Initialize the diagnostics status
            status = DiagnosticStatus()
            status.name = "Laptop Battery"

	    current_battery_level = random.randint(1, 100)

	    if current_battery_level < error_battery_level:
		status.message = "Low " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.ERROR
	    elif current_battery_level < warn_battery_level:
		status.message = "Warning " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.WARN     
	    else:
		status.message = "OK " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.OK
            
            # Add the raw battery level to the diagnostics message
            status.values.append(KeyValue("Level", str(current_battery_level)))
            
            # Build the diagnostics array message
            msg = DiagnosticArray()
            msg.header.stamp = rospy.Time.now()
            msg.status.append(status)

            return msg


if __name__ == '__main__':
    # The intial battery level - 100 is considered full charge
    initial_battery_level = 100

    # Error battery level for diagnostics
    error_battery_level = 10

    # Warn battery level for diagnostics
    warn_battery_level = 20

    rospy.init_node('simulator2')

    pub = rospy.Publisher('/diagnostics', DiagnosticArray)
    
    loop = 0
    my_rate = rospy.Rate(1)

    while not rospy.is_shutdown():
	if ((loop % 30) == 0):
            msg = motor()
            msg2 = battery()
            msg3 = temperature()
            msg4 = laser()
            msg5 = camera()
            msg6 = laptop_battery()
            print '#################################################'
            print 'Loop started ' + str(loop)
	    #print msg
	    #print msg2
            print '#################################################'

        pub.publish(msg)
        pub.publish(msg2)
        pub.publish(msg3)
        pub.publish(msg4)
        pub.publish(msg5)
        pub.publish(msg6)
        loop = loop + 1
        my_rate.sleep()
