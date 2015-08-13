#!/bin/bash
########################################################################
# Configuration
apache_ip="feliperoman.com.br"
########################################################################

clear
echo ===================================================================
echo Starting Native Host Simulator auto configuration
echo ===================================================================

#Ask user iteration
echo ===================================================================
echo "Apache HTTP IP address: $apache_ip"
echo ===================================================================

#Assign existing hostname to $hostn
hostn=$(cat /etc/hostname)

#Display existing hostname
echo ===================================================================
echo "Current hostname is $hostn"
echo ===================================================================

#Get IP Address
echo ===================================================================
ip=`ifconfig|xargs|awk '{print $7}'|sed -e 's/[a-z]*:/''/'`
echo "Current IP address is $ip"
echo ===================================================================

#Send http post to add this host to Nagios
echo ===================================================================
echo "Add VM to Nagios - Send http with network information"
mkdir temp -p
cd temp
URL_BASE="$apache_ip/mestrado/apache/add.php?hostname=$hostn&ip=$ip"
echo "HTTP Server $apache_ip"
wget "http://${URL_BASE}" --quiet
cd ..
echo ===================================================================

#Press a key to reboot
echo ===================================================================
echo "Done. Run ./start_simulator.bash to start a Native simulator"
cd ~
./start_simulator.bash
echo ===================================================================
