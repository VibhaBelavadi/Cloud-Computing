__author__ = 'Vedashree'

import os
import subprocess
import sys
import re

filename = "data_vcpu.txt"
file_path = "/home/node4_a1/data_vcpu.txt"
maximum = 0
current = 0

def convertKibToMb(KIB):
      memoryInMB=float(KIB) * 0.001024
      return memoryInMB

def map_hostip_hostname(hostip):
    hostInfoFile="/home/node4_a1/hostInfo.txt"
    with open(hostInfoFile) as f:
        for i, line in enumerate(f,1):
            currentLine=line.split("|")
            if(currentLine[0].strip()== hostip):
                print currentLine[1]

def memory_check():
        hostip = str("192.168.1.33")
	map_hostip_hostname(hostip)

memory_check()
