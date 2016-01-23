#!/bin/bash/
#Get the VM's CPU information from the VM machine, Veda Output style

rm -f /home/node4_a1/DC/OutputV2.txt

while read LINE
do
	arrIn=(${LINE//|/ })
	
	#ping -c 1 ${arrIn[0]} &> /dev/null && var="success" || var="fail"
	#if [ $var == "success" ]; then
		
	#connect to virtual machine
	ssh -n root@${arrIn[0]} top -bn 2 > /home/node4_a1/DC/CPUutilV.txt
	ssh -n root@${arrIn[0]} free -m > /home/node4_a1/DC/memTestV.txt
		
	#CPU utilisation
	var=$( sed -n '/%Cpu/p' /home/node4_a1/DC/CPUutilV.txt | sed '2!d' | egrep -o "[0-9]+(\.[0-9][0-9]?)?" | sed '1!d' )
		
	#memory utilisation
	mem_used=$( sed '2!d' /home/node4_a1/DC/memTestV.txt | egrep -o "[0-9]+" | sed '2!d' )
	mem_total=$( sed '2!d' /home/node4_a1/DC/memTestV.txt | egrep -o "[0-9]+" | sed '1!d' )
	mem_per=$((100 * $mem_used / $mem_total))

	
	#Dominfo file content
	if [ ${arrIn[2]} == "192.168.1.40" ]; then
		virsh dominfo ${arrIn[1]} > /home/node4_a1/DC/d.txt
	else
		ssh -n root@${arrIn[2]} virsh dominfo ${arrIn[1]} > /home/node4_a1/DC/d.txt
	fi

	mem_cur=$( sed '9!d' /home/node4_a1/DC/d.txt | egrep -o "[0-9]+" )
       	mem_max=$( sed '8!d' /home/node4_a1/DC/d.txt | egrep -o "[0-9]+" )

	echo "${arrIn[0]}|$var|$mem_per|$mem_cur|$mem_max" >> /home/node4_a1/DC/OutputV2.txt
		
	rm -f /home/node4_a1/DC/CPUutilV.txt
	rm -f /home/node4_a1/DC/memTestV.txt
	rm -f /home/node4_a1/DC/d.txt
	#else
	#	echo "Fail!"
	#fi
done < /home/node4_a1/VmInfo.txt
