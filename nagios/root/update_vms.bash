#!/bin/bash
clear
echo ===================================================================
echo "Update VM list"
echo "Require root login"
echo ===================================================================


echo ===================================================================
read -p "Apache IP address: " -e -i feliperoman.com.br host
echo ===================================================================

echo ===================================================================
echo "Restore /etc/hosts from /etc/hosts.orig" 
cp /etc/hosts.orig /etc/hosts
echo ===================================================================

echo ===================================================================
echo "Download VMs list"
cd ~
wget -c "$host/mestrado/apache/dump.php" --
echo ===================================================================

echo ===================================================================
echo "Configure VMs list"
cat dump.php
cat dump.php >> /etc/hosts
rm /root/dump.php
echo ===================================================================

echo ===================================================================
echo "Download Nagios CFG files from VMs"
cd ~
rm -rf temp
mkdir temp
cd temp
wget -r --no-parent http://$host/mestrado/apache/cfg
cd $host
cd mestrado
cd apache
cd cfg
cp *.cfg /etc/nagios3/conf.d
cd /etc/nagios3/conf.d
chmod 755 *
cd ~
/etc/init.d/nagios3 restart
echo ===================================================================
