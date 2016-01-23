#!/bin/bash/
#Given the host's IP, echo the CPU utilisation

val1="192.168.1.33"
val2="192.168.1.40"
val3="node3"
val4="node4"
val5="master"
val6="192.168.1.88"

while read LINE
do
	arrIn=(${LINE// / })
	if [ "$1" == "$val1" ]; then
		if [ "${arrIn[0]}" == "$val3" ]; then
			echo "${arrIn[1]}" >> GetHostCPUOut.txt;
		fi
	if [ "$1" == "$val2" ]; then
		if [ "${arrIn[0]}" == "$val4" ]; then
			echo "${arrIn[1]}" >> GetHostCPUOut.txt;
		fi
	fi
	if [ "$1" == "$val6" ]; then
		if [ "${arrIn[0]}" == "$val5" ]; then
			echo "${arrIn[1]}" >> GetHostCPUOut.txt;
		fi
	fi
done < /home/Data.txt
cpuidle=`sed -n '3p' /home/node4_a1/GetHostCPUOut.txt`;
#cpuutil=`expr 100 \\- $cpuidle`;
echo $cpuidle;
