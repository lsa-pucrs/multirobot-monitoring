#!/usr/bin/env python

import roslib; # roslib.load_manifest('pr2_motors_analyzer')

import rospy, random
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

if __name__ == '__main__':
    rospy.init_node('pr2_motor_power_sim')

    pub = rospy.Publisher('/diagnostics', DiagnosticArray)
    
    array = DiagnosticArray()
    # Fake motor 1
    motor1 = DiagnosticStatus(name = 'Motor 1', level = 0, 
                                  message = 'Running')
    motor1.values = [ KeyValue(key = 'Runstop hit', value = 'False'),
                          KeyValue(key = 'Estop hit', value = 'False')]

    # Fake motor 2
    motor2 = DiagnosticStatus(name = 'Motor 2', level = 0, 
                                  message = 'Running')
    motor2.values = [ KeyValue(key = 'Runstop hit', value = 'False'),
                          KeyValue(key = 'Estop hit', value = 'False')]


    # Fake EtherCAT Master status, all OK
    eth_stat = DiagnosticStatus(name='EtherCAT Master', level = 0,
                                message = 'OK')

    # Fake Temperature
    #temperature = random.randint(1, 80)
    #temp = DiagnosticStatus("Temperature " + str(temperature), level = 0,
    #                            message = 'OK')


    # Fake temperature
    status = DiagnosticStatus()
    status.name = "Battery Level"

    # Set the diagnostics status level based on the current battery level
    # The intial battery level - 100 is considered full charge
    initial_battery_level = 100

    # Error battery level for diagnostics
    error_battery_level = 20

    # Warn battery level for diagnostics
    warn_battery_level = 50

    # Initialize the current level variable to the startup level
    current_battery_level = initial_battery_level

    # Initialize the new level variable to the startup level
    new_battery_level = initial_battery_level

    # The step sized used to decrease the battery level on each publishing loop
    #battery_step = float(initial_battery_level)
    current_battery_level = random.randint(1, 80)

    if current_battery_level < error_battery_level:
        status.message = "Low Battery"
        status.level = DiagnosticStatus.ERROR
    elif current_battery_level < warn_battery_level:
        status.message = "Medium Battery"
        status.level = DiagnosticStatus.WARN     
    else:
        status.message = "Battery OK"
        status.level = DiagnosticStatus.OK
    
    # Add the raw battery level to the diagnostics message
    status.values.append(KeyValue("Battery Level", str(current_battery_level)))


    array.status = [ motor1, motor2, eth_stat, status ]

    my_rate = rospy.Rate(1.0)
    while not rospy.is_shutdown():
        pub.publish(array)
        my_rate.sleep()

