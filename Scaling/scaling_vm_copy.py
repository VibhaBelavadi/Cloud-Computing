import time       
import subprocess 
import re
import sys
sys.path.insert(0, '/home/node4_a1/')
import scaling_utilites as sc
from VM_migrate import Migrate

file_name = "/home/node4_a1/DC/OutputV2.txt"
threshold = 88
vm_list = []
vm_cpuUtilization = {}
vm_duplicate_cpuUtilization = {}
mem_treshold = 75
low_mem_treshold = 5
flag_treshold=0



def readOutput():
	getDataCmd= "sh /home/node4_a1/DC/VMVeda2.sh"
	subprocess.check_call(getDataCmd,shell=True)
        print "Generated output"

def readGanglia():
    """
        This function open and reads data file from ganglia
        The data file is of the format ip_addr||cpu_utilization
        It parses the file and if at any point the cpu_utilization crosses threshold,
        it adds it to a dictionary if not previously present
        """
    with open(file_name) as f:
        print "Opened file"
        for line in f.readlines():
            line_words = line.split('|')
            value = float(line_words[1].rstrip('\n'))
            cpu_utilization = float(value)
            value = float(line_words[2].rstrip('\n'))
            mem_utilization = float(value)
            if cpu_utilization > threshold:
                key_cpu = line_words[0]+"CPU"
                if key_cpu in vm_cpuUtilization:
                    length_of_values = len(vm_cpuUtilization[key_cpu])
                    size = 3
                    if length_of_values < int(size):
                        vm_cpuUtilization[key_cpu][0] = cpu_utilization
                        vm_cpuUtilization[key_cpu].append(time.time())
                    else:
			 if vm_cpuUtilization[key_cpu][1] == 0 and vm_cpuUtilization[key_cpu][2] == 0:
                            vm_cpuUtilization[key_cpu][0]= cpu_utilization
                            vm_cpuUtilization[key_cpu][1] = time.time()
                            vm_cpuUtilization[key_cpu][2] = time.time()
                         else:
                            vm_cpuUtilization[key_cpu][0] = cpu_utilization
                            vm_cpuUtilization[key_cpu][2] = time.time()
                else:
                    vm_cpuUtilization.setdefault(key_cpu, []).append(cpu_utilization)
                    vm_cpuUtilization[key_cpu].append(time.time())

	    if mem_utilization > mem_treshold:
                key_mem = line_words[0]+"MEM"
	    	if key_mem in vm_cpuUtilization:
	            length_of_values = len(vm_cpuUtilization[key_mem])
		    size = 3
                    if length_of_values < int(size):
                        vm_cpuUtilization[key_mem][0] = mem_utilization
                        vm_cpuUtilization[key_mem].append(time.time())
                    else:
			if vm_cpuUtilization[key_mem][1]== 0 and vm_cpuUtilization[key_mem][2] == 0:
			    vm_cpuUtilization[key_mem][0]= mem_utilization
                            vm_cpuUtilization[key_mem][1] = time.time()
                            vm_cpuUtilization[key_mem][2] = time.time()
			else: 
                            vm_cpuUtilization[key_mem][0] = mem_utilization
                            vm_cpuUtilization[key_mem][2] = time.time()
                else:
                    vm_cpuUtilization.setdefault(key_mem,[]).append(mem_utilization)
                    vm_cpuUtilization[key_mem].append(time.time())

           if mem_utilization < low_ mem_treshold:
                key_mem = line_words[0]+"MEM"
                if key_mem in vm_cpuUtilization:
                    length_of_values = len(vm_cpuUtilization[key_mem])
                    size = 3
                    if length_of_values < int(size):
                        vm_cpuUtilization[key_mem][0] = mem_utilization
                        vm_cpuUtilization[key_mem].append(time.time())
                    else:
                        if vm_cpuUtilization[key_mem][1]== 0 and vm_cpuUtilization[key_mem][2] == 0:
                            vm_cpuUtilization[key_mem][0]= mem_utilization
                            vm_cpuUtilization[key_mem][1] = time.time()
                            vm_cpuUtilization[key_mem][2] = time.time()
                        else:
                            vm_cpuUtilization[key_mem][0] = mem_utilization
                            vm_cpuUtilization[key_mem][2] = time.time()
                else:
                    vm_cpuUtilization.setdefault(key_mem,[]).append(mem_utilization)
                    vm_cpuUtilization[key_mem].append(time.time()) 

def scaling():
    
    for key in vm_cpuUtilization:
	print key
	for values in vm_cpuUtilization[key]:
            print values
    for key in vm_cpuUtilization:
        length_of_values = len(vm_cpuUtilization[key])
        size = 3
        if length_of_values >int(size)-1:
            diff = vm_cpuUtilization[key][2]-vm_cpuUtilization[key][1]
            compare_time =  int(diff)
            if "CPU" in key:
                if vm_cpuUtilization[key][0] > threshold:
                    flag_treshold = 1
	    if "MEM" in key:
		if vm_cpuUtilization[key][0] > mem_treshold:
                    flag_treshold = 1
                if vm_cpuUtilization[key][0] < low_mem_treshold:
                    flag_treshold = 1
            if compare_time >= 60 and flag_treshold:
		if "CPU" in key:
                #CallScaling(key)
		    check_for_scaling(key,"CPU")
		    vm_cpuUtilization[key][1]=0
                    vm_cpuUtilization[key][2]=0
                    flag_treshold = 0
		if "MEM" in key:
                    print "Mem Treshold reached for node"+key
                    check_for_scaling(key,"MEM")
                    vm_cpuUtilization[key][1]=0
                    vm_cpuUtilization[key][2]=0
                    flag_treshold = 0
                print("\n")
                #print "Reset timers for scaled values"
                #for key in vm_cpuUtilization:
                    #print key
                    #for values in vm_cpuUtilization[key]:
                        #print values
                flag_treshold = 0
            if compare_time == 0:
	       vm_cpuUtilization[key][1] = time.time()
               vm_cpuUtilization[key][2] = time.time()
    time.sleep(20)



def check_for_scaling(key,status):
     print "Status"+status
     host_cpuutilization = 0
     host_memutilization = 0
     #print "Treshold reached for node"+key
     host_ip =sc.check_resources_host(key)
     #print "Main Scaling"+str(host_ip)
     ip = sc.strip_key_IP(key)
     flag_stage = sc.check_if_ip_excluded(ip)
     if flag_stage:
         print "IP present in file migration_exclusion"
     else:
         print "IP is not present"
         if status == "CPU":
             host_cpuutilization=sc.check_HOST_CPU_Utilization(host_ip)
             if host_cpuutilization==0:
	         print "CPU Utilization is low and perform Scaling"
                 sc.CallScaling(ip,status)
             else:
                 print "CPU Utiilization is high  and perform migration"
                 #Migrate(str(ip),status)
         elif status == "MEM":
             if vm_cpuUtilization[key][0] > mem_treshold:
                 host_memutilization=sc.check_HOST_Mem_Utilization(host_ip)
                 if host_memutilization  == 0:
                     used_memory = sc.check_mem_scaling_vm(key)
                     print "Host Memory Utilization is low and perform scaling of VM "+str(used_memory)
                     #if float(used_memory) > 0:
                         #sc.scaling_memory(key,status,used_memory)
                 else:
                     print "Host Memory Utilization is high migrate to another VM"
                     #Migrate(str(ip),status)
             else:
                 print "Scale down VM"
         host_memutilization = 0
         host_cpuutilization = 0

def scaling_check():
        while(1):
            #readOutput()
            readGanglia()
            scaling()
scaling_check()
