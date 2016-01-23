#!/usr/bin/python
import time
import sys
import subprocess
import datetime
from VM_migrate import Migrate
def main():
        while True:
                print("Host Patroling Starts")
		print("CPU Check")
                obj=IsTimeUP()
                hostfile="/home/node4_a1/hostInfo.txt"
                with open(hostfile) as f:
                        for line in f:
                                ipindex = line.index("|")
                                hostipaddr=line[:ipindex]
                                #Check for CPU
                                cmdgetcpu="ssh root@"+hostipaddr+" top -bn 2 | sed -n '/%Cpu(s)/p' | sed '2!d' | egrep -o \"[0-9]+(\.[0-9][0-9]?)?\" | sed '1!d'"
                                hostcpuutil=subprocess.check_output(cmdgetcpu,shell=True)
                                hostcpuutil = hostcpuutil.decode('utf-8')
                                if float(hostcpuutil) < 60 and obj.isPresent(hostipaddr,"CPU"):
                                    obj.remove(hostipaddr,"CPU")
                                if float(hostcpuutil) >= float(60):
                                        obj.add(hostipaddr,"CPU")
                                        print("Host with high CPU"+hostipaddr)
                                        if obj.doMigrate(hostipaddr,"CPU"):
                                            vmfile="/home/node4_a1/VmInfo.txt"
                                            vmtomigrate=""
                                            subprocess.check_call("sh /home/node4_a1/DC/VMKaran1.sh",shell=True)
					    maxcpu=0
                                            with open(vmfile) as fvmlist:
                                                for vmlistline in fvmlist:
                                                    if hostipaddr in vmlistline:
                                                        ipindex = vmlistline.index("|")
                                                        vmipaddr = vmlistline[:ipindex]
                                                        print("Checking VM"+vmipaddr)
                                                        vmutilfile="/home/node4_a1/DC/OutputK1.txt"
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
                                                obj.remove(hostipaddr,"CPU")
                                                Migrate(str(vmtomigrate),"CPU")
                                #Check for Memory
                                time.sleep(10)
				print("Memory Check")
                                cmdgetmem="ssh root@"+hostipaddr+" free | grep Mem | awk '{print $3/$2 * 100}'"
                                hostmemutil=subprocess.check_output(cmdgetmem,shell=True)
                                hostmemutil = hostmemutil.decode('utf-8')
                                #print("mem util "+hostmemutil)
                                #hostmemutil=80
                                if float(hostmemutil) < 70 and obj.isPresent(hostipaddr,"MEM"):
                                    obj.remove(hostipaddr,"MEM")
                                if float(hostmemutil) >= float(70):
                                    obj.add(hostipaddr,"MEM")
                                    if obj.doMigrate(hostipaddr,"MEM"):
                                        vmfile="/home/node4_a1/VmInfo.txt"
                                        vmtomigrate=""
					subprocess.check_call("sh /home/node4_a1/DC/VMKaran1.sh",shell=True)
                                        maxmem=0
                                        with open(vmfile) as fvmlist:
                                            for vmlistline in fvmlist:
                                                if hostipaddr in vmlistline:
                                                   ipindex = vmlistline.index("|")
                                                   vmipaddr = vmlistline[:ipindex]
                                                   vmutilfile="/home/node4_a1/DC/OutputK1.txt"
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
                                            obj.remove(hostipaddr,"MEM")
                                            Migrate(vmtomigrate,"MEM")

class IsTimeUP(object):
    timeCheckDict={}
    def add(self, host, Param):
        key=str(host)+str(Param)
        val = self.timeCheckDict.get(key)
        if val is None:
            print("adding")
            self.timeCheckDict[key]=datetime.datetime.now()

    def isPresent(self, host, Param):
        key=str(host)+str(Param)
        val = self.timeCheckDict.get(key)
        if val is not None:
            return True
        else:
            return False

    def doMigrate(self, host, Param):
        print("Checking time diff for"+host)
        key=str(host)+str(Param)
        entrytime=self.timeCheckDict[key]
        diff =datetime.datetime.now() - entrytime
        if diff.seconds >= 300:
            return True
        else:
            return False

    def remove(self, host, Param):
        key=str(host)+str(Param)
        val = self.timeCheckDict.get(key)
        if val is not None:
            del self.timeCheckDict[key]

if __name__=="__main__":
        main()
