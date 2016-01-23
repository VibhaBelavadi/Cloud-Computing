import sys
import subprocess

def scaling(node_name,ip,used_memory):
    scaled_memory =int(used_memory) + 50000
    print "trying to scale"
    cmd = "ssh root@"+ip+" sh /home/node4_a1/Scaling/scale_up_mem.sh "+ node_name+" "+str(scaled_memory)
    output=subprocess.check_output(cmd,shell=True)
    out_text = output.decode('utf-8')
    print out_text

def scaling_mem(): 
    node_name = sys.argv[1]
    ip = sys.argv[2] 
    used_memory = sys.argv[3]
    print "USED MEM " + str(used_memory)
    scaling(node_name,ip,used_memory)
    print "Memory Scaling completed for"+ip

def DeleteFromFile(VMIP):
   fileName = "/home/node4_a1/MigrationExclusion.txt"
   f = open(fileName,"r+")
   d = f.readlines()
   f.seek(0)
   for i in d:
    if VMIP.strip() not in i.strip():
     f.write(i)
   f.truncate()
   f.close()
    
scaling_mem()




