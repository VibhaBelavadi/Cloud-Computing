#!/bin/bash/
#Get the VM's CPU information from the VM machine, Veda Output style

rm -f /home/node4_a1/DC/OutputV1.txt
rm -f /home/node4_a1/DC/test.txt
rm -f /home/node4_a1/DC/t.txt
rm -f /home/node4_a1/DC/d.txt

while read LINE
do
	arrIn=(${LINE//|/ })
	
	ping -c 1 ${arrIn[0]} &> /dev/null && var="success" || var="fail"
	if [ $var == "success" ]; then
		
		echo "${arrIn[0]}"
		#connect to virtual machine
		ssh -n root@${arrIn[0]} '
	       
		var=$( top -bn 2 | sed -n '/%Cpu/p' | sed '2!d' | egrep -o "[0-9]+(\.[0-9][0-9]?)?" | sed '1!d' )
		echo "cpu"
		mem_used=$( free -m | sed '2!d' | egrep -o "[0-9]+" | sed '2!d' )
		echo "mem1"
		mem_total=$( free -m | sed '2!d' | egrep -o "[0-9]+" | sed '1!d' )
		echo $mem_used
		echo $mem_total
		mem_per=$((100 * $mem_used / $mem_total))
                echo $mem_per
		echo "$var|$mem_per" > /home/test.txt
		echo "yes"
		'

		scp root@${arrIn[0]}:/home/test.txt /home/node4_a1/DC
		varia=$( sed -n 1p /home/node4_a1/DC/test.txt )

		if [ ${arrIn[2]} == "192.168.1.40" ]; then
			virsh dominfo ${arrIn[1]} > /home/node4_a1/DC/d.txt
		else
			ssh -n root@${arrIn[2]} virsh dominfo ${arrIn[1]} > /home/node4_a1/DC/d.txt
		fi

		mem_cur=$( sed '9!d' /home/node4_a1/DC/d.txt | egrep -o "[0-9]+" )
                mem_max=$( sed '8!d' /home/node4_a1/DC/d.txt | egrep -o "[0-9]+" )

		echo "${arrIn[0]}|$varia|$mem_cur|$mem_max" >> /home/node4_a1/DC/t.txt
	fi
done < /home/node4_a1/VmInfo.txt
