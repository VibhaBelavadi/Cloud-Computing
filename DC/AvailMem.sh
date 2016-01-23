#!/bin/bash/
#Available memory for host machine

while read LINE
do
arrIn=(${LINE//|/ })
ssh root@${arrIn[0]} '
#Get the available memory
memory=$(free -m | sed '2!d' | egrep -o "[0-9]+" | sed '6!d')
hostnme=$(hostname)
echo $(hostname)|$memory > /home/datum.txt
scp /home/datum.txt root@node4:/home/datum.txt
'
info=$(head -n1 /home/node4_a1
done < /home/node4_a1/hostInfo.txt
