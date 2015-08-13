#!/usr/bin/env python

import roslib; # roslib.load_manifest('pr2_motors_analyzer')

import rospy, random, md5
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

########################################################################
# Configuration
########################################################################

########################################################################
# Simulation config
total_errors = 0
total_warnings = 0

########################################################################
# Refresh interval in seconds
refresh_interval = 300


########################################################################
# Robot configuration
########################################################################

########################################################################
# Motors config
number_of_motors = 3

########################################################################
# Temperature config
number_of_sensors = 2

########################################################################
# Laser config
number_of_lasers = 2


########################################################################
# Cameras config
number_of_cameras = 1


########################################################################
# Initial runtime setup
########################################################################

########################################################################
# Battery config
# The intial battery level - 100 is considered full charge
initial_battery_level = 100

# Error battery level for diagnostics
error_battery_level = 10

# Warn battery level for diagnostics
warn_battery_level = 20

# Runtime error control
current_errors = 0
current_warnings = 0

def motor(msg):
	global current_errors
	global current_warnings
	for cont in range(1,number_of_motors + 1):
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
			current_warnings += 1
		else:
			status.message = 'Stopped'
			status.level = DiagnosticStatus.ERROR
			current_errors += 1
		msg.status.append(status)
	return msg

def camera(msg):
	global current_errors
	global current_warnings
	for cont in range(1,number_of_cameras + 1):
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
			current_warnings += 1
		else:
			status.message = 'Error'
			status.level = DiagnosticStatus.ERROR
			current_errors += 1
		msg.status.append(status)    
	return msg


def temperature(msg):
	global current_errors
	global current_warnings
	for cont in range(1,number_of_sensors + 1):
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
			current_warnings += 1
		else:
			temp = random.randint(80, 99)
			status.message = str(temp) + ' degrees'
			status.level = DiagnosticStatus.ERROR
			current_errors += 1
		msg.status.append(status)
	return msg

def laser(msg):
	global current_errors
	global current_warnings
	for cont in range(1,number_of_lasers + 1):
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
			current_warnings += 1
		else:
			status.message = 'Error'
			status.level = DiagnosticStatus.ERROR
			current_errors += 1
		msg.status.append(status)
	return msg


def battery(msg):
	global current_errors
	global current_warnings
	# Initialize the diagnostics status
	status = DiagnosticStatus()
	status.name = "Robot Battery"

	current_battery_level = random.randint(1, 100)

	if current_battery_level < error_battery_level:
		status.message = "Low " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.ERROR
		current_errors += 1
	elif current_battery_level < warn_battery_level:
		status.message = "Warning " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.WARN
		current_warnings += 1
	else:
		status.message = "OK " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.OK
		
	# Add the raw battery level to the diagnostics message
	status.values.append(KeyValue("Level", str(current_battery_level)))	
	msg.status.append(status)
	return msg

def laptop_battery(msg):
	global current_errors
	global current_warnings
	# Initialize the diagnostics status
	status = DiagnosticStatus()
	status.name = "Laptop Battery"

	current_battery_level = random.randint(1, 100)

	if current_battery_level < error_battery_level:
		status.message = "Low " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.ERROR
		current_errors += 1
	elif current_battery_level < warn_battery_level:
		status.message = "Warning " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.WARN
		current_warnings += 1     
	else:
		status.message = "OK " + str(current_battery_level) + "%"
		status.level = DiagnosticStatus.OK
		
	# Add the raw battery level to the diagnostics message
	status.values.append(KeyValue("Level", str(current_battery_level)))
	msg.status.append(status)
	return msg

def generate_values_internal(msg):
	global current_errors
	global current_warnings
	
	msg.header.stamp = rospy.Time.now()
	msg = motor(msg)
	msg = battery(msg)
	msg = temperature(msg)
	msg = laser(msg)
	msg = camera(msg)
	msg = laptop_battery(msg)
	return msg

def generate_values():
	global total_errors
	global total_warnings
	global current_errors
	global current_warnings
	
	msg = DiagnosticArray()
	loop2 = 0

	while True:
		loop2 = loop2 + 1
		current_errors = 0
		current_warnings = 0
		generate_values_internal(msg)
		print '#################################################'
		print 'Generate_values runtime count ' + str(loop2)
		#print 'total_errors = ' + str(total_errors)
		#print 'current_errors = ' + str(current_errors)
		#print 'total_warnings = ' + str(total_warnings)
		#print 'current_warnings = ' + str(current_warnings)
		print '#################################################'
		
		# Avoid stuck the simulator
		if (loop2 > 100000):
			break
		
		if (total_warnings == current_warnings):
			if (total_errors == current_errors):
				#print "match"
				break
	return msg

def update_config():
	global total_errors
	global total_warnings 
	global refresh_interval
	global number_of_motors
	global number_of_sensors
	global number_of_lasers
	global number_of_cameras
	total_errors = 0
	total_warnings = 0
	return False


if __name__ == '__main__':
	# Create initial values
	rospy.init_node('simulator3')
	pub = rospy.Publisher('/diagnostics', DiagnosticArray)	
	loop = 0
	my_rate = rospy.Rate(1)
	update_config()

	while not rospy.is_shutdown():
		#print "loop = " + str(loop)
		#print "refresh_interval = " + str(refresh_interval)
		if ((loop % refresh_interval) == 0):
			print '#################################################'
			print 'Refresh interval ' + str(refresh_interval) + ' seconds...'
			msg = generate_values()
			#print msg
			print '#################################################'

		# Check if the config was changed, if yes force reload sensor values
		if (update_config() == True):
			print '#################################################'
			print 'Simulator configuration updated sucessfully'
			print '#################################################'
			msg = generate_values()

		pub.publish(msg)
		loop = loop + 1
		my_rate.sleep()
