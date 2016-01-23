#!/bin/bash/
#Given the VMip as input, echo the cpu utilisation

while read LINE
do
	arrIn=(${LINE//||/ })
	if [ "${arrIn[0]}" == "$1" ]; then
		echo "${arrIn[1]}" 
	fi
done < /home/node4_a1/Scaling/output.txt
