#!/usr/bin/python

import  sys

import subprocess

import time

from VM_getIP import getGuestIP

class PhysicalMachine(object):

   'Common base class for all PhyscialMachine'

   def __init__(self,mem,IO,cpu,IP,hostName):

     self.avaliableMemory =mem

     self.avaliablediskIO=IO

     self.CPUuseage=cpu

     self.IPaddress=IP

     self.hostName=hostName





def convertKibToMb(KIB):

      memoryInMB=float(KIB) * 0.001024

      return memoryInMB



def gethostIP(hostName):

    hostInfoFile="/home/node4_a1/hostInfo.txt"
    
    with open(hostInfoFile) as f:

        for i, line in enumerate(f,1):
	   	
            currentLine=line.split("|")
	    	
            if(currentLine[1].strip()==hostName):

                return currentLine[0]







def getTargetHost(userMemory,userIO,userCPU,CPUMEMFlag):

    getDataCmd= "sh /home/node4_a1/DC/ioscript.sh "

    subprocess.check_call(getDataCmd,shell=True)

    userMemoryInMb=convertKibToMb(userMemory)

    file_name="/home/node4_a1/DC/Data.txt"

    lineCount=0

    PMList=[]

    PotentialPMList=[]

    PMmemory=0.0

    PMCPU=0.0

    PMdiskIO=0.0

    IPaddress=""

    hostName=""

    with open(file_name) as f:

        for i, line in enumerate(f, 1):

            lineCount= lineCount+1
	    

            line_words=line.split(' ')

            if lineCount == 3 :

                PMCPU=line_words[1]
	
                IPaddress=gethostIP(line_words[0])
                	

                hostName=line_words[0]

                PMList.append(PhysicalMachine(PMmemory,PMdiskIO,PMCPU,IPaddress,hostName))

                lineCount=0



            elif lineCount ==1:

              PMdiskIO=line_words[1]

            elif lineCount ==2:

                PMmemory=line_words[1]

            else:

                lineCount=0

    

    for currentPM in PMList:
        
       
        if(float(currentPM.avaliableMemory) > float(userMemoryInMb)  and int(userCPU) <= 8):
	    
            PotentialPMList.append(currentPM)



    

    if(len(PotentialPMList)==0):

       return ""

    elif(len(PotentialPMList)==1):

       return(PotentialPMList[0].IPaddress)

    else:

        if(CPUMEMFlag=="CPU"):

            targetHost=PotentialPMList[0]

            if(len(PotentialPMList) >=1):

                for PM in PotentialPMList:

                    if(float(targetHost.CPUuseage) > float(PM.CPUuseage)):

                         targetHost=PM

            return(targetHost.IPaddress)

        elif(CPUMEMFlag=="MEM"):

            targetHost=PotentialPMList[0]

            if(len(PotentialPMList) >=1):

                for PM in PotentialPMList:

                    if(float(targetHost.avaliableMemory) < float(PM.avaliableMemory)):

                        targetHost=PM

            return(targetHost.IPaddress)



if __name__ == '__main__':

   ipadd= getTargetHost(1000000,17,1,"MEM")
   print("finally" + ipadd)








