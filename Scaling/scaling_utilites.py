import time
import subprocess
import re

def getVMHostIP(IPaddress):
    VMInfoFile="/home/node4_a1/VmInfo.txt"
    with open(VMInfoFile) as f:
        for i, line in enumerate(f,1):
            currentLine=line.split("|")
            if(currentLine[0].strip()==IPaddress):
                return currentLine[2].strip()


def check_resources_host(IPAddress):
    ip=re.sub("[a-zA-Z]","",str(IPAddress))
    print ip
    host_ip=getVMHostIP(ip)
    return host_ip


def check_if_ip_excluded(vmIP):
    flag = 0
    checkvmfile="/home/node4_a1/MigrationExclusion.txt"
    if vmIP not in open(checkvmfile).read():
        #hs = open(checkvmfile,"a")
        #hs.write("{}\n".format(vmIP))
        #hs.close()
	return flag
    else:
	flag = 1
        return flag

def write_to_file(VMIP):
    checkvmfile="/home/node4_a1/MigrationExclusion.txt"
    hs = open(checkvmfile,"a")
    hs.write("{}\n".format(VMIP))
    hs.close()


def strip_key_IP(IPAddr):
    ip=re.sub("[a-zA-Z]","",str(IPAddr))
    return ip

def check_HOST_CPU_Utilization(hostIP):
    cmdgetcpu="ssh root@"+hostIP+" top -bn 2 | sed -n '/%Cpu(s)/p' | sed '2!d' | egrep -o \"[0-9]+(\.[0-9][0-9]?)?\" | sed '1!d'"
    hostcpuutil=subprocess.check_output(cmdgetcpu,shell=True)
    hostcpuutil = hostcpuutil.decode('utf-8')
    if float(hostcpuutil) >= float(85):
      return 1
    else:	
      return 0


def check_HOST_Mem_Utilization(hostIP):
    cmdgetmem="ssh root@"+hostIP+" free | grep Mem | awk '{print $3/$2 * 100}'"
    hostmemutil=subprocess.check_output(cmdgetmem,shell=True)
    hostmemutil = hostmemutil.decode('utf-8')
    if float(hostmemutil) >= float(85):
       return 1
    else:    
       return 0

def CallScaling(key,status):
    VMFilePath = "/home/node4_a1/VmInfo.txt"
    with open(VMFilePath) as f:
        for i, line in enumerate(f, 1):
            line_words=line.split('|')
            if(line_words[0]==key):
                if(status == "CPU"):
                    scaleCmd = "python parse_vcpu.py " + line_words[1] + " " + line_words[2]
                    subprocess.check_call(scaleCmd,shell=True)
                print("VM_NAME" + str(line_words[1]) + " " + "host IP "+ str(line_words[2]))


def check_mem_scaling_vm(ip):
    file_name="/home/node4_a1/DC/OutputV2.txt"
    ip = strip_key_IP(ip)
    with open(file_name) as f:
        print "opened"
        for line in f.readlines():
            line_words = line.split('|') 
            if( str(line_words[0].strip()) == str(ip.strip())):
                used_memory = line_words[3]
                max_memory = line_words[4]
                if(float(max_memory) - float(used_memory) > 60000):
		    return used_memory
    return 0

def scaling_memory(key,status,used_memory):
     VMFilePath = "/home/node4_a1/VmInfo.txt"
     key = strip_key_IP(key)
     with open(VMFilePath) as f:
         for i, line in enumerate(f, 1):
             line_words=line.split('|')
             if(line_words[0]==key):
                  if(status == "MEM"):
                       print("VM_NAME"+str(line_words[1]) + " " + "host IP "+ str(line_words[2]).strip()+" "+used_memory.strip())
                       scaleCmd = "python scaling_mem.py " + line_words[1] + " " + line_words[2].strip()+" "+used_memory.strip()
                       subprocess.check_call(scaleCmd,shell=True)
                  
                       
