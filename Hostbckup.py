#!/usr/bin/python
import time
import sys
import subprocess
from VM_migrate import Migrate
def main():
        while True:
                print("Host Patroling Starts")
		time.sleep(1)
                hostfile="/home/node4_a1/hostInfo.txt"
                with open(hostfile) as f:
                        for line in f:
                                ipindex = line.index("|")
                                hostipaddr=line[:ipindex]
                                #Check for CPU
                                cmdgetcpu="ssh root@"+hostipaddr+" top -bn 2 | sed -n '/%Cpu(s)/p' | sed '2!d' | egrep -o \"[0-9]+(\.[0-9][0-9]?)?\" | sed '1!d'"
                                hostcpuutil=subprocess.check_output(cmdgetcpu,shell=True)
                                hostcpuutil = hostcpuutil.decode('utf-8')
                                #hostcpuidle = 10
                                if float(hostcpuutil) >= float(20):
                                        print("Host with high CPU"+hostipaddr)
					vmfile="/home/node4_a1/VmInfo.txt"
                                        vmtomigrate=""
					subprocess.check_call("sh /home/node4_a1/DC/VMKaran1.sh",shell=True)
                                        with open(vmfile) as fvmlist:
                                            for vmlistline in fvmlist:
                                                if hostipaddr in vmlistline:
                                                    maxcpu=0
                                                    ipindex = vmlistline.index("|")
                                                    vmipaddr = vmlistline[:ipindex]
                                                    print("Checking VM"+vmipaddr")
						    vmutilfile="/home/node4_a1/DC/OutputK.txt"
                                                    with open(vmutilfile) as fvmutil:
                                                        for linevmutil in fvmutil:
                                                            if vmipaddr in linevmutil:
                                                                words = linevmutil.split("|")
                                                                if maxcpu < float(words[1]):
                                                                    maxcpu=float(words[1])
                                                                    vmtomigrate=vmipaddr
                                                                    break
                                        checkvmfile="/home/node4_a1/MigrationExclusion.txt"
                                        if vmtomigrate not in open(checkvmfile).read():
                                            hs = open(checkvmfile,"a")
                                            hs.write("{}\n".format(vmtomigrate))
                                            hs.close()
					    print("VM to migrate cpu "+vmtomigrate)
                                            Migrate(str(vmtomigrate),"CPU")
                                #Check for Memory
                                time.sleep(60)
                                cmdgetmem="ssh root@"+hostipaddr+" free | grep Mem | awk '{print $3/$2 * 100}'"
                                hostmemutil=subprocess.check_output(cmdgetmem,shell=True)
                                hostmemutil = hostmemutil.decode('utf-8')
                                #print("mem util "+hostmemutil)
				#hostmemutil=80
                                if float(hostmemutil) >= float(75):
                                    vmfile="/home/node4_a1/VmInfo.txt"
                                    vmtomigrate=""
				    subprocess.check_call("sh /home/node4_a1/DC/VMKaran1.sh",shell=True)
                                    with open(vmfile) as fvmlist:
                                        for vmlistline in fvmlist:
                                            if hostipaddr in vmlistline:
                                               maxmem=0
                                               ipindex = vmlistline.index("|")
                                               vmipaddr = vmlistline[:ipindex]
                                               vmutilfile="/home/node4_a1/DC/OutputK.txt"
                                               with open(vmutilfile) as fvmutil:
                                                   for linevmutil in fvmutil:
                                                       if vmipaddr in linevmutil:
                                                           words = linevmutil.split("|")
                                                           if maxmem < float(words[2]):
                                                               maxmem=float(words[2])
                                                               vmtomigrate=vmipaddr
                                                               break
                                    checkvmfile="/home/node4_a1/MigrationExclusion.txt"
                                    if vmtomigrate not in open(checkvmfile).read():
                                        hs = open(checkvmfile,"a")
                                        hs.write("{}\n".format(vmtomigrate))
                                        hs.close()
                                        print("VM to migrate memory"+vmtomigrate)
					Migrate(vmtomigrate,"MEM")
if __name__=="__main__":
        main()
