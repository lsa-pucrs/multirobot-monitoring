#!/bin/bash
########################################################################
# Configuration
apache_ip="feliperoman.com.br"
INTERVAL="60"  # update interval in seconds
IF=$(ifconfig | grep 'eth' | awk '{print $1}')
HOSTNAME=$(cat /etc/hostname)
IP=`ifconfig|xargs|awk '{print $7}'|sed -e 's/[a-z]*:/''/'`
#echo $IF
########################################################################


while true
do

        ########################################################################
        # CPU
        CPU=$(dc -e "`cut -d' ' -f1 < /proc/loadavg` 100 * p")
        #echo "CPU = $CPU"
        ########################################################################


        ########################################################################
        # Memory
        FREE_DATA=`free -m | grep Mem` 
        CURRENT=`echo $FREE_DATA | cut -f3 -d' '`
        TOTAL=`echo $FREE_DATA | cut -f2 -d' '`
        memory=$(echo "scale = 2; $CURRENT/$TOTAL*100" | bc)
        echo "Memory = $memory"
        
        ########################################################################
        
        
        ########################################################################
        # Bandwidth
        R1=`cat /sys/class/net/$IF/statistics/rx_bytes`
        T1=`cat /sys/class/net/$IF/statistics/tx_bytes`
        sleep $INTERVAL
        R2=`cat /sys/class/net/$IF/statistics/rx_bytes`
        T2=`cat /sys/class/net/$IF/statistics/tx_bytes`
        TBPS=`expr $T2 - $T1`
        RBPS=`expr $R2 - $R1`
        TKBPS=`expr $TBPS / 1024`
        RKBPS=`expr $RBPS / 1024`
        TOTAL=`expr $TKBPS + $RBPS`
        RBPS=`expr $TOTAL / 1024`
        #echo "TX $1: $TKBPS kB/s RX $1: $RKBPS kB/s"
        #echo "Bandwidth = $TOTAL"
        ########################################################################
        
        ########################################################################
        # HTTP data
        echo ===================================================================
        echo "Send status information"
        mkdir temp -p
        cd temp
        URL_BASE="$apache_ip/mestrado/apache/status.php?hostname=$HOSTNAME&ip=$IP&memory=$memory&bandwidth=$TOTAL&cpu=$CPU"
        echo "HTTP Server $apache_ip"
        echo $URL_BASE
        wget "http://${URL_BASE}" --quiet
        cd ..
        echo ===================================================================


        ########################################################################
        
done
