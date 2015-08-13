#!/bin/bash
########################################################################
# Configuration

########################################################################
clear
echo "==================================================================="
echo "Install VM Simulator"
echo "*** Root login required ***"
echo "==================================================================="

echo "==================================================================="
read -p "Enter SSH host for download RSA key: " -e -i "corfu.pucrs.br" host
echo "Download RSA key: $host"
ssh-keyscan -H "corfu.pucrs.br" >> /root/.ssh/known_hosts
#ssh "corfu.pucrs.br"
echo "==================================================================="


echo "==================================================================="
read -p "Enter VM Guest path for download: " -e -i "froman@corfu.pucrs.br:/dados/froman/simulator_vm/imagem.vdi" vm_image
echo "Download URL: $vm_image"
vdi_image=${vm_image##*/}
echo "Image VDI file: $vdi_image"
echo "==================================================================="

echo ===================================================================
read -p "Enter new VM Guest name: " -e -i vm-lsa-simulator-1 vm_name
echo "VM Guest name: $vm_name"
echo ===================================================================

echo ===================================================================
echo "Start download"
cd /root
mkdir -p $vm_name
cd $vm_name
apt-get install sshpass -qq
#echo "***********************************"
#echo "Download disabled for test purposes"
#echo "***********************************"
sshpass -p "novasenha" scp $vm_image /root/$vm_name/$vdi_image
echo ===================================================================

echo ===================================================================
echo "Remove previous VM: /root/VirtualBox VMs/$vm_name"
rm -rf "/root/VirtualBox VMs/$vm_name"
echo ===================================================================

echo ===================================================================
echo "Creating and Starting VM"
VBoxManage createvm --register --name $vm_name --ostype Linux
echo ===================================================================
echo "Add IDE storage"
VBoxManage storagectl $vm_name --name "IDE Controller" --add ide
echo ===================================================================
echo "Configure $vdi_image disk"
VBoxManage modifyvm $vm_name --hda /root/$vm_name/$vdi_image
echo ===================================================================
echo "Configure 2048 memory"
VBoxManage modifyvm $vm_name --memory 2048
echo ===================================================================
echo "Configure bridge network"
VBoxManage modifyvm $vm_name --nic1 bridged --bridgeadapter1 'eth0' 
echo ===================================================================
echo "Start vm_name"
VBoxManage startvm $vm_name
echo ===================================================================
