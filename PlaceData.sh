#!bin/bash
#script to get CPU data from both the nodes

sh /home/node4_a1/ioscript.sh
scp /home/Data.txt root@192.168.1.33:/home
ssh root@192.168.1.33 sh /home/node4_a1/ioscript.sh && exit
