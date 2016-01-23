#!/usr/bin/python

import  sys

import subprocess

import time

from VM_Placement import getTargetHost

__author__ = 'Supriya'





if __name__ == '__main__':

    userMemory = sys.argv[2]
    userId= sys.argv[1];	
    userIO= sys.argv[3];

    userCPU=sys.argv[4]

    vmName=sys.argv[5];

    vmID=sys.argv[6];
    numberofArguments= len(sys.argv);
    vmbaseImagePath="";
    if(numberofArguments > 7): 
      vmbaseImagePath=sys.argv[7];

    if str(vmbaseImagePath) !="":
      baseImagePath =vmbaseImagePath
    else:
      baseImagePath="/home/node4_a1/baseImg.qcow2"

    
    guestConfigurationPath="/home/node4_a1/Config_WithTokens.xml"

    targetHostIP=getTargetHost(userMemory,userIO,userCPU,"CPU")

    

    if str(targetHostIP) != "":

        createCmd = "sh /home/node4_a1/createvm.sh " + vmName + " " +  vmID + " " + userMemory + " " + userCPU + " " + baseImagePath + " " + guestConfigurationPath + " " + targetHostIP
        subprocess.check_call(createCmd,shell=True)

        time.sleep(80)

        IPaddr="ssh root@"+ str(targetHostIP) +" sh /home/node4_a1/RetrieveIP.sh " + vmName

        iprecieved=subprocess.check_output(IPaddr,shell=True)

        out_text = iprecieved.decode('utf-8')
        
	print"ip:"+str(out_text)
        
	output_file = open("/home/node4_a1/VmInfo.txt" ,'a+')

        datatoWrite= str(out_text).strip() + "|" + vmName + "|" + targetHostIP+"|"+userId

        output_file.write(datatoWrite)

        output_file.write("\n")
        subprocess.check_call("sh /home/node4_a1/Ganglia/gangInst1.sh "+str(out_text).strip(),shell=True)
