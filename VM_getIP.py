#!/usr/bin/python

import subprocess


def getGuestIP(vmName):
       IPaddr = "ssh root@192.168.1.33 sh /home/node4_a1/RetrieveIP.sh " +vmName
       c= subprocess.check_call(IPaddr,shell=True)
       return c
