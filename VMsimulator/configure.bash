#!/bin/bash
########################################################################
# Configuration
apache_ip="feliperoman.com.br"
########################################################################

clear
echo ===================================================================
echo Starting VM Simulator auto configuration
echo ===================================================================

#Ask user iteration
echo ===================================================================
#read -p "Enter HTTP Server IP address: " -e -i 10.32.177.28 apache_ip
#read -p "Enter Nagios Server IP address: " -e -i 10.32.177.40 nagios_ip
echo "Apache HTTP IP address: $apache_ip"
#echo "Nagios IP address: $nagios_ip"
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

#Create hostname
echo ===================================================================
original_string=$ip
string_to_replace='.'
string_to_replace_with='_'
newhost="lsa-vm-simulator-${original_string//$string_to_replace/$string_to_replace_with}"
#display new hostname
echo "New hostname is $newhost"
echo ===================================================================


#Send http post to add this host to Nagios
echo ===================================================================
echo "Add VM to Nagios - Send http with network information"
mkdir temp -p
cd temp
URL_BASE="$apache_ip/mestrado/apache/add.php?hostname=$newhost&ip=$ip"
echo "HTTP Server $apache_ip"
wget "http://${URL_BASE}" --quiet
cd ..
echo ===================================================================

#change hostname in /etc/hosts & /etc/hostname
echo ===================================================================
echo "Update OS hostname"
sudo sed -i "s/$hostn/$newhost/g" /etc/hosts
sudo sed -i "s/$hostn/$newhost/g" /etc/hostname
echo ===================================================================

#Press a key to reboot
echo ===================================================================
if [ "$hostn" == "$newhost" ]; then
	echo "VM already configured"
	read -s -n 1 -p "Press any key to reboot"
else
	echo "Restart Guest OK"
	read -s -n 1 -p "Press any key to reboot"
	sudo reboot
fi