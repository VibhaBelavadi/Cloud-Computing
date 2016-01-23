__author__ = 'Vedashree'
import os
import string
import re
import subprocess
import sys


filename = "maxinfo.txt"
current_vcpu = 0

def DeleteFromFile(VMIP,fileName):
   fileName = "/home/node4_a1/MigrationExclusion.txt"
   f = open(fileName,"r+")
   d = f.readlines()
   f.seek(0)
   for i in d:
    if VMIP.strip() not in i.strip():
     f.write(i)
   f.truncate()
   f.close()

def execute_scaling(node_name,ip):
        print "In execute scaling:"+str(current_vcpu)
	cmd = "ssh root@"+ip+" sh /home/node4_a1/scale_up_vm.sh "+ node_name+" "+str(current_vcpu)
 	output=subprocess.check_output(cmd,shell=True)
	out_text = output.decode('utf-8')
	print out_text

def  check_if_possible(node_name,ip):
	cmd = "ssh root@"+ip+" python /home/node4_a1/check_scalability.py "+node_name
	output=subprocess.check_output(cmd,shell=True)
	out_text = output.decode('utf-8')
	global current_vcpu
	current_vcpu = int(out_text)
   	if(current_vcpu > 0):
		execute_scaling(node_name,ip)
	else:
		print "Scaling not possible"

def execute():
	node_name= sys.argv[1]
	ip = sys.argv[2]
	check_if_possible(node_name,ip)
	#execute_scaling(node_name,ip)

execute()
