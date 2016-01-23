#!/bin/bash/
#Get the VM's CPU information from the VM machine, Karan Output style the original file

rm -f /home/node4_a1/DC/OutputK1.txt

while read LINE
do
	#echo "$LINE"
	arrIn=(${LINE//|/ })
	#echo "1"
	ping -c 1 ${arrIn[0]} &> /dev/null && var="success" || var="fail"
	if [ $var == "success" ]; then
		#echo "${arrIn[0]}"		
		ssh -n root@${arrIn[0]} top -bn 2 > /home/node4_a1/DC/CPUutilK.txt
		ssh -n root@${arrIn[0]} free -m > /home/node4_a1/DC/memTestK.txt
		
		#get the CPU utilisation
		var=$( sed -n '/%Cpu/p' /home/node4_a1/DC/CPUutilK.txt | sed '2!d' | egrep -o "[0-9]+(\.[0-9][0-9]?)?" | sed '1!d' )
		#get the memory value
		memory=$( sed '2!d' /home/node4_a1/DC/memTestK.txt | egrep -o "[0-9]+" | sed '2!d' )

		#store the values in stat file and delete unnecessary files
		echo "${arrIn[0]}|$var|$memory" >> /home/node4_a1/DC/OutputK1.txt

		rm -f /home/node4_a1/DC/CPUutilK.txt
		rm -f /home/node4_a1/DC/memTestK.txt
	else
		echo "Fail!"
	fi
done < /home/node4_a1/VmInfo.txt
