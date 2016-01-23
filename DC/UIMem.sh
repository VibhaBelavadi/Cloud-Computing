#!/bin/bash
#Get the memory assigned to that VM, need for UI

while read LINE
do
        arrIn=(${LINE//|/ })

        ping -c 1 ${arrIn[0]} &> /dev/null && var="success" || var="fail"
        if [ $var == "success" ]; then
		if [ ${arrIn[0]} == $1 ]; then
                	if [ ${arrIn[2]} == "192.168.1.40" ]; then
                        	virsh dominfo ${arrIn[1]} > /home/node4_a1/DC/d.txt
                	else
                        	ssh -n root@${arrIn[2]} virsh dominfo ${arrIn[1]} > /home/node4_a1/DC/d.txt
                	fi
			
			mem_cur=$( sed '9!d' /home/node4_a1/DC/d.txt | egrep -o "[0-9]+" )
                	echo "$mem_cur"
		fi
        fi
done < /home/node4_a1/VmInfo.txt
