#!/bin/bash
#Generate graphs
#read from the file and create the directory


#print the metric for a day
MAIN_DIR="/home/node4_a1/graphs/"
GANG_DIR='/var/lib/ganglia/rrds/Cloud123/'
CPU_RRD='/cpu_user.rrd'
MEM_RRD='/mem_free.rrd'
DSK_RRD='/disk_free.rrd'
File=$1

ssh node3 "

while read LINE
do
	arrIn=(${LINE//|/ })
	if [ "$File" == "/home/node4_a1/VmInfo.txt" ]; then
                 lin=${arrIn[0]}
        fi
	if [ "$File" == "/home/node4_a1/hostInfo.txt" ]; then
                 lin=${arrIn[1]}
        fi
	DATA_DIR=${MAIN_DIR}${lin}
	mkdir -p -- "$DATA_DIR"
	#CPU Metric for a minute
	rrdtool graph ${DATA_DIR}/cpu_user_five_min.png --end now --start end-300s --width 500 DEF:ds0a=${GANG_DIR}${lin}/cpu_user.rrd:sum:AVERAGE AREA:ds0a#ABCDEF:"Area of CPU Utilisation/l"
	#CPU Metric for an hour
	rrdtool graph ${DATA_DIR}/cpu_user_hour.png --end now --start end-3600s --width 500 DEF:ds0b=${GANG_DIR}${lin}/cpu_user.rrd:sum:AVERAGE AREA:ds0b#ABCDEF:"Area of CPU Utilisation for an hour/l"
	#CPU metric for a day
	rrdtool graph ${DATA_DIR}/cpu_user_day.png --end now --start end-86400s --width 500 DEF:ds0c=${GANG_DIR}${lin}/cpu_user.rrd:sum:AVERAGE AREA:ds0c#ABCDEF:"Area of CPU Utilisation for a day/l"

	#Memory Metric for a minute
        rrdtool graph ${DATA_DIR}/mem_free_five_min.png --end now --start end-300s --width 500 DEF:ds0d=${GANG_DIR}${lin}/mem_free.rrd:sum:AVERAGE AREA:ds0d#ABCDEF:"Area of CPU Utilisation/l"
        #Memory Metric for an hour
        rrdtool graph ${DATA_DIR}/mem_free_hour.png --end now --start end-3600s --width 500 DEF:ds0e=${GANG_DIR}${lin}/mem_free.rrd:sum:AVERAGE AREA:ds0e#CC00FF:"Area of CPU Utilisation for an hour/l"
        #Memory metric for a day
        rrdtool graph ${DATA_DIR}/mem_free_day.png --end now --start end-86400s --width 500 DEF:ds0f=${GANG_DIR}${lin}/mem_free.rrd:sum:AVERAGE AREA:ds0f#CC00FF:"Area of CPU Utilisation/l"
	#Disk Metric for 5 minutes
        rrdtool graph ${DATA_DIR}/disk_free_five_min.png --end now --start end-300s --width 500 DEF:ds0g=${GANG_DIR}${lin}/disk_free.rrd:sum:AVERAGE AREA:ds0g#CC00FF:"Area of CPU Utilisation/l"
        #Disk Metric for an hour
        rrdtool graph ${DATA_DIR}/disk_user_hour.png --end now --start end-3600s --width 500 DEF:ds0h=${GANG_DIR}${lin}/disk_free.rrd:sum:AVERAGE AREA:ds0h#DD00AA:"Area of CPU Utilisation for an hour/l"
        #Disk metric for a day
        rrdtool graph ${DATA_DIR}/disk_user_day.png --end now --start end-86400s --width 500 DEF:ds0i=${GANG_DIR}${lin}/disk_free.rrd:sum:AVERAGE AREA:ds0i#DD00AA:"Area of CPU Utilisation/l"
	
done < $File

"
