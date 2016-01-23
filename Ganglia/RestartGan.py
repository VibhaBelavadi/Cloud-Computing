#!/usr/bin/python

import sys
import subprocess

if __name__ == '__main__':

	subprocess.check_call("sh /home/node4_a1/Ganglia/RestartGan.sh /home/node4_a1/hostInfo.txt", shell=True)
	subprocess.check_call("sh /home/node4_a1/Ganglia/RestartGan.sh /home/node4_a1/Ganglia/VmInfo.txt", shell=True)
