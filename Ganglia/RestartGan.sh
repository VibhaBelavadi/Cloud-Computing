#!/bin/bash
#Restart Ganglia gmond gmetad everywhere

#Variable file name
file_name=$1

while read LINE
do
	arrIn=(${LINE//|/ })
	#echo "${arrIn[0]}"
	ping -c 1 ${arrIn[0]} &> /dev/null && var="success" || var="fail"
	if [ $var == "success" ]; then
		ssh root@${arrIn[0]} '
			systemctl restart gmond
			echo "Ys!"
		'
	fi
done < $file_name

service gmetad restart
