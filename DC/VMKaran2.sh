#!/bin/bash/
#Get the VM's CPU information from the VM machine, Karan Output style the original file

rm -f /home/node4_a1/DC/OutputK2.txt

while read LINE
do
	arrIn=(${LINE//|/ })
	ssh -n root@${arrIn[0]} top -bn 2 > /home/node4_a1/DC/CPUutilK2.txt
	ssh -n root@${arrIn[0]} free -m > /home/node4_a1/DC/memTestK2.txt
		
	#get the CPU utilisation
	var=$( sed -n '/%Cpu/p' /home/node4_a1/DC/CPUutilK2.txt | sed '2!d' | egrep -o "[0-9]+(\.[0-9][0-9]?)?" | sed '1!d' )
	#get the memory value
	memory=$( sed '2!d' /home/node4_a1/DC/memTestK2.txt | egrep -o "[0-9]+" | sed '2!d' )

	#store the values in stat file and delete unnecessary files
	echo "${arrIn[0]}|$var|$memory" >> /home/node4_a1/DC/OutputK2.txt

	rm -f /home/node4_a1/DC/CPUutilK2.txt
	rm -f /home/node4_a1/DC/memTestK2.txt

done < /home/node4_a1/VmInfo.txt
