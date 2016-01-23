__author__ = 'Vedashree'

import os
import subprocess
import sys
import re

filename = "data_vcpu.txt"
file_path = "/home/node4_a1/data_vcpu.txt"
maximum = 0
current = 0

def read_vcpu_info():
    f=open(filename,"r")
    line1=f.readline()
    global maximum
    maximum= re.sub("\D","",line1)
    line2=f.readline()
    global current
    current= re.sub("\D","",line2)
    f.close()     

def cpu_virsh(nodename):
        cmd = "virsh vcpucount "+nodename
        output=subprocess.check_output(cmd,shell=True)
        out_text = output.decode('utf-8')
        output_file = open(filename,'w')
        output_file.write(out_text)
        output_file.write("\n")
	output_file.close()
        read_vcpu_info()
	global maximum
	global current
	current = int(current)
        if int(maximum)-1 > int(current):
		print current+1
	else:
        	print 0

def vcpu_check():
        virtual_name = sys.argv[1]
        #virtual_name = "nodetwo"
        cpu_virsh(virtual_name)

vcpu_check()


