#!/bin/bash
#Generate graphs
#read from the file and create the directory

rm -rf /home/node4_a1/graphs

cat /home/node4_a1/hostInfo.txt >> /home/node4_a1/gang.txt
cat /home/node4_a1/VmInfo.txt >> /home/node4_a1/gang.txt

scp /home/node4_a1/gang.txt root@node3:/home

ssh root@node3 sh GangGraphs.sh

scp -r root@node3:/home/graphs /home/node4_a1

mv /home/node4_a1/graphs/node0 /home/node4_a1/graphs/192.168.1.10
mv /home/node4_a1/graphs/node1 /home/node4_a1/graphs/192.168.1.20
mv /home/node4_a1/graphs/node2 /home/node4_a1/graphs/192.168.1.30
mv /home/node4_a1/graphs/node3 /home/node4_a1/graphs/192.168.1.31
mv /home/node4_a1/graphs/node4 /home/node4_a1/graphs/192.168.1.40
mv /home/node4_a1/graphs/master /home/node4_a1/graphs/192.168.1.88

rm -f /home/node4_a1/gang.txt
