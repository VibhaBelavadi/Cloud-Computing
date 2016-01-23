import time
import subprocess

file_name = "output.txt"
threshold = 30
vm_list = []
vm_cpuUtilization = {}


def readGanglia():
    """
        This function open and reads data file from ganglia
        The data file is of the format ip_addr||cpu_utilization
        It parses the file and if at any point the cpu_utilization crosses threshold,
        it adds it to a dictionary if not previously present
        """
    with open(file_name) as f:
        for line in f.readlines():
            line_words = line.split('||')
            value = float(line_words[1].rstrip('\n'))
            cpu_utilization = float(100.00-value)
            if cpu_utilization > threshold:
                if line_words[0] in vm_cpuUtilization:
                    length_of_values = len(vm_cpuUtilization[line_words[0]])
                    size = 3
                    if length_of_values < int(size):
                        vm_cpuUtilization[line_words[0]][0] = cpu_utilization
                        vm_cpuUtilization[line_words[0]].append(time.time())
                    else:
                        vm_cpuUtilization[line_words[0]][0] = cpu_utilization
                        vm_cpuUtilization[line_words[0]][2] = time.time()
                else:
                    vm_cpuUtilization.setdefault(line_words[0], []).append(cpu_utilization)
                    vm_cpuUtilization[line_words[0]].append(time.time())


def scaling():
    #print "Here"
    for key in vm_cpuUtilization:
        length_of_values = len(vm_cpuUtilization[key])
        size = 3
        if length_of_values >int(size)-1:
            diff = vm_cpuUtilization[key][2]-vm_cpuUtilization[key][1]
            compare_time =  int(diff)
            if compare_time >= 120:
                CallScaling(key)
                vm_cpuUtilization.pop(key,None)
    time.sleep(20)

def CallScaling(key):
    VMFilePath = "/home/node4_a1/VmInfo.txt"
    with open(VMFilePath) as f:
        for i, line in enumerate(f, 1):
            line_words=line.split('|')
            if(line_words[0]==key):
                #scaleCmd = "sh parsevcpu.sh " + line_words[1] + " " + line_words[2]
                #subprocess.check_call(scaleCmd,shell=True)
                print("VM_NAME" + str(line_words[1]) + " " + "host IP "+ str(line_words[2]))


def scaling_check():
        while(1):
                readGanglia()
                scaling()
scaling_check()
