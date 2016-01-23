#!/bin/bash/
#script to print hostips linewise in output file Script1Output.txt

while read LINE
do
	arrIn=(${LINE//|/ })
	echo "${arrIn[0]}" >> GetHostsIPOut.txt
done < /home/node4_a1/hostInfo.txt 
