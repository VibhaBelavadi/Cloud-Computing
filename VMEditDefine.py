#!/usr/bin/python
import fileinput
import sys
import subprocess
import datetime
import time

def main():
    editParameterInXML("192.168.1.14","CPU",2)
    time.sleep(5)
    defineVM("192.168.1.14")

def editParameterInXML(vmip,param,value):
    print(datetime.datetime.now())
    toprintlogs="Edit xml parameter request received for vm ip "+vmip+" and for parameter "+param+" with value "+str(value)
    print(toprintlogs)
    vmname=""
    vminfofile="/home/node4_a1/VmInfo.txt"
    with open(vminfofile) as fvmlist:
        for vmlistline in fvmlist:
            if vmip in vmlistline:
                words = vmlistline.split("|")
                vmname = words[1]
                vmname = vmname.strip()
    vmxmlfile="/home/guestdata/"+vmname+"/Config_WithTokens.xml"
    print(vmxmlfile)
    if param == "CPU":
        searchExp="vcpu placement='static'"
        replaceExp="<vcpu placement='static' current='"+str(value)+"'>8</vcpu>"+'\n'
        for line in fileinput.input(vmxmlfile, inplace=1):
            if searchExp in line:
                line = line.replace(line,replaceExp)
            sys.stdout.write(line)
	    #print("Edit successful")
    if param == "MEM":
        searchExp="currentMemory unit='KiB'"
        replaceExp="<currentMemory unit='KiB'>"+str(value)+"</currentMemory>"+'\n'
        for line in fileinput.input(vmxmlfile, inplace=1):
            if searchExp in line:
                line = line.replace(line,replaceExp)
            sys.stdout.write(line)
	    #print("Edit successful")

def defineVM(vmip):
    print(datetime.datetime.now())
    toprintlogs="Define VM request received for vm "+vmip
    vminfofile="/home/node4_a1/VmInfo.txt"
    with open(vminfofile) as fvmlist:
        for vmlistline in fvmlist:
            if vmip in vmlistline:
                words = vmlistline.split("|")
                vmname = words[1]
		vmname = vmname.strip()
		hostipaddr = words[2]
		hostipaddr = hostipaddr.strip()
		vmxmlfile="/home/guestdata/"+vmname+"/Config_WithTokens.xml"
		targetloc="/home/node4_a1/define/"+vmname+".xml"
                cmd="sh DefineVM.sh "+vmname+" "+hostipaddr
                print(cmd)
		statusreceived=subprocess.check_output(cmd,shell=True)
		statusreceived = statusreceived.decode('utf-8')
		statusreceived = str(statusreceived).strip()
		print(statusreceived)
		#if(statusreceived == '0'):
		#	print("Success")
		#else:
		#	print("Error in DefineVM.sh")
if __name__=="__main__":
        main()
