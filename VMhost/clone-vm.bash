#!/bin/bash
########################################################################
# Configuration

########################################################################
clear
echo "==================================================================="
echo "Clone VM Simulator"
echo "*** Root login *NOT* required ***"
echo "Virtual Machine vm-lsa-simulator-1 must be created first."
echo "If not created yet run install_simulator.bash to install the first VM."
echo "==================================================================="

for counter in 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
do
	echo "==================================================================="
	#read -p "Enter new VM Guest name: " -e -i vm-lsa-simulator-$counter vm_name
	vm_name=vm-lsa-simulator-$counter
	echo "New VM Guest name: $vm_name"
	echo "==================================================================="

	echo "==================================================================="
	echo "Remove previous VM: /home/lsa/VirtualBox VMs/$vm_name"
	rm -rf "/home/lsa/VirtualBox VMs/$vm_name"
	echo "==================================================================="

	echo "==================================================================="
	echo "Clone"
	VBoxManage clonevm vm-lsa-simulator-1 --name $vm_name --register
	echo "==================================================================="

	echo "==================================================================="
	echo "Start vm_name"
	VBoxManage startvm $vm_name
	echo "==================================================================="

done


