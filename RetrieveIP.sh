#!/bin/bash
expect /home/node4_a1/ConsoleForIP.exp $1 > "/home/node4_a1/$1.out"
ip=$( sed -n '3p' "/home/node4_a1/$1.out")
echo $ip
