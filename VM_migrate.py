#!/usr/bin/python

import subprocess
import fileinput
import sys

from VM_Placement import getTargetHost



def getVMName(IPaddress):

    VMInfoFile="/home/node4_a1/VmInfo.txt"
    with open(VMInfoFile) as f:
        for i, line in enumerate(f,1):
            currentLine=line.split("|")
            if(currentLine[0].strip()==IPaddress):
                return currentLine[1].strip()



def getVMHostIP(IPaddress):
    VMInfoFile="/home/node4_a1/VmInfo.txt"
    with open(VMInfoFile) as f:
        for i, line in enumerate(f,1):
            currentLine=line.split("|")
            if(currentLine[0].strip()==IPaddress):
                return currentLine[2].strip()


def ReplaceVMInfoFile(VMIPaddress,targetHostIP,oldHostIP):
    VMInfoFile="/home/node4_a1/VmInfo.txt"
    with open(VMInfoFile) as f:
        for i, line in enumerate(f,1):
            currentLine=line.split("|")
	    if(currentLine[0].strip()==VMIPaddress.strip()):
		print "Updating config files"
	        VMName=currentLine[1].strip()
		UserId=currentLine[3].strip()	
                DeleteFromFile(VMIPaddress,"/home/node4_a1/VmInfo.txt")
    		newData=VMIPaddress.strip()+"|"+VMName+"|"+targetHostIP.strip()+"|"+UserId.strip()
    		AddVMInfo(newData)        	


def DeleteFromFile(VMIP,fileName):
   f = open(fileName,"r+")
   d = f.readlines()
   f.seek(0)
   for i in d:
    if VMIP.strip() not in i.strip():
     f.write(i)
   f.truncate()
   f.close()

def AddVMInfo(datatoWrite):
   output_file = open("/home/node4_a1/VmInfo.txt" ,'a+')
   output_file.write(datatoWrite)
   output_file.write("\n")


def Migrate(VMIPAddress,CPUMEMFlag):
 VMName = getVMName(VMIPAddress)
 VMHostIP=getVMHostIP(VMIPAddress)
 getDataCmd= "sh /home/node4_a1/DC/VMDominfo.sh " + VMName + " " + VMHostIP
 outputreceived=subprocess.check_output(getDataCmd,shell=True)
 out_text = outputreceived.decode('utf-8')
 print("data received" + str(out_text))
 data=str(out_text).split("|")
 targetHostIP =getTargetHost(float(data[1]),17,float(data[0]),CPUMEMFlag)
 print(targetHostIP) 

 if((targetHostIP!="") and (targetHostIP.strip() != VMHostIP.strip())) :
 	migrateCmd= "sh /home/node4_a1/migratevm.sh "+ VMName.strip() + " " + VMHostIP.strip() + " " + targetHostIP.strip()
 	statusreceived=subprocess.check_output(migrateCmd,shell=True)
 	out_text = statusreceived.decode('utf-8')
	print("output" + str(out_text).strip())
	if((str(out_text).strip())=="0"):
	    ReplaceVMInfoFile(VMIPAddress,targetHostIP.strip(),VMHostIP.strip())
            DeleteFromFile(VMIPAddress.strip(),"/home/node4_a1/MigrationExclusion.txt")
        else:
            DeleteFromFile(VMIPAddress.strip(),"/home/node4_a1/MigrationExclusion.txt")
 else:
  	DeleteFromFile(VMIPAddress.strip(),"/home/node4_a1/MigrationExclusion.txt")

if __name__ == '__main__':

   ipadd= Migrate("192.168.1.29","CPU")
   

