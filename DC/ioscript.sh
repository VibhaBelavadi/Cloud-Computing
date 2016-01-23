#!/bin/bash/
#script to get the data

rm -f /home/node4_a1/DC/Data.txt

while read LINE
do
	arrIn=(${LINE//|/ })
	ping -c 1 ${arrIn[0]} &> /dev/null && var="success" || var="fail"
	if [ $var == "success" ]; then
		hostnme=${arrIn[1]}
		ssh  -o StrictHostKeyChecking=no -n root@$hostnme '
	
		rm -f /home/datum.txt

		mem=$( free -m | sed '2!d' | egrep -o "[0-9]+" | sed '6!d' )

		dsk=$( df -h --total | sed '8!d' | egrep -o "[0-9]+" | sed '3!d' )

		cpu=$( top -bn 2 | sed -n '/%Cpu/p' | sed '2!d' | egrep -o "[0-9]+(\.[0-9][0-9]?)?" | sed '1!d' )

		echo "$(hostname) $dsk" >> /home/datum.txt
		echo "$(hostname) $mem" >> /home/datum.txt
		echo "$(hostname) $cpu" >> /home/datum.txt
	'
		scp ${arrIn[0]}:/home/datum.txt /home/node4_a1/DC
		cat /home/node4_a1/DC/datum.txt >> /home/node4_a1/DC/Data.txt

		rm -f /home/node4_a1/DC/datum.txt
	fi
done < /home/node4_a1/hostInfo.txt
