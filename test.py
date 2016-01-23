#!/usr/bin/python
import time
import  sys
import subprocess
def main():
	while True:
		time.sleep(10)
		hostfile= "/home/node4_a1/hostInfo.txt"
		with open(hostfile) as f:
			for line in f:
				ipindex = line.index("|")
				ipaddr=line[:ipindex]
				cmdgetcpu="ssh root@"+ipaddr+" mpstat | grep all | awk '{print $13}'"
				print(cmdgetcpu)
				cpuutil=subprocess.check_output(cmdgetcpu,shell=True)
				cpuutil = cpuutil.decode('utf-8')
				print(cpuutil)
			   
if __name__=="__main__":
	main()
