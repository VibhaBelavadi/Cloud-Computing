#!/bin/bash/
#Give the host's IP, list the VM's IP


while read LINE
do
	arrIn=(${LINE//|/ })
	if [ "${arrIn[2]}" == "$1" ]; then
		echo "${arrIn[0]}" >> /home/node4_a1/GetVMIPOut.txt;
	fi
done < /home/node4_a1/VmInfo.txt

