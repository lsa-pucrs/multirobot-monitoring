#!/bin/bash
########################################################################
# Configuration

########################################################################
clear
echo "==================================================================="
echo "Install VM Simulator"
echo "==================================================================="

echo "==================================================================="
#read -p "Enter SSH host for download RSA key: " -e -i "corfu.pucrs.br" host
host="corfu.pucrs.br"
echo "Download RSA key: $host"
##########################################################
ssh-keyscan -H "corfu.pucrs.br" >> /home/lsa/.ssh/known_hosts
echo "Accept SSH key and quit without login..."
echo "Manual step required: Open a new window and run: ssh corfu.pucrs.br"
echo "Accept the RSA key and continue from here..."
#ssh "corfu.pucrs.br"
echo "==================================================================="

echo "==================================================================="
read -p "Enter VM Guest path for download: " -e -i "froman@corfu.pucrs.br:/dados/froman/simulator_vm/imagem.vdi" vm_image
echo "Download URL: $vm_image"
vdi_image=${vm_image##*/}
echo "Image VDI file: $vdi_image"
echo "==================================================================="

echo "==================================================================="
read -p "Enter new VM Guest name: " -e -i vm-lsa-simulator-1 vm_name
echo "VM Guest name: $vm_name"
echo "==================================================================="

echo "==================================================================="
echo "Start download"
cd ~
mkdir -p $vm_name
cd $vm_name
#sudo apt-get install sshpass -qq
echo "***********************************"
echo "Download disabled for test purposes"
echo "***********************************"
##########################
# Local test
#sshpass -p "novasenha" scp $vm_image /home/lsa/$vm_name/$vdi_image
#cp ~/$vm_name/imagem.vdi .
##########################
echo "==================================================================="

echo "==================================================================="
cd ~
echo "Download and install clone-vm.bash"
wget -c http://feliperoman.com.br/mestrado/VMhost/clone-vm.bash
chmod 777 clone-vm.bash
echo "==================================================================="

echo "==================================================================="
echo "Remove previous VM: /home/lsa/VirtualBox VMs/$vm_name"
rm -rf "/home/lsa/VirtualBox VMs/$vm_name"
echo "==================================================================="

echo "==================================================================="
echo "Creating and Starting VM"
VBoxManage createvm --register --name $vm_name --ostype Linux
echo "==================================================================="
echo "Add IDE storage"
VBoxManage storagectl $vm_name --name "IDE Controller" --add ide
echo "==================================================================="
echo "Configure $vdi_image disk"
VBoxManage modifyvm $vm_name --hda /home/lsa/$vm_name/$vdi_image
echo "==================================================================="
echo "Configure 256MB memory"
VBoxManage modifyvm $vm_name --memory 256
echo "==================================================================="
echo "Configure bridge network"
VBoxManage modifyvm $vm_name --nic1 bridged --bridgeadapter1 'eth0' 
echo "==================================================================="
echo "Start vm_name"
VBoxManage startvm $vm_name
echo "==================================================================="

