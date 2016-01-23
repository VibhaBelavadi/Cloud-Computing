#import os
#import iptools
#import ipaddress
import random
import sys
import subprocess

ip_list = []
iprange = []

def read_file():
    lines = open('used_ip.txt').readlines()
    lines[:] = lines[2:]
    lines[:] = lines[:-3]
    spl = []
    global ip_list
    for line in lines:         # for loop on file object returns one line at a time
        spl = line.strip().split() # split the line at whitespaces, str.split returns a list
        ip_list.append(spl[0]) # append the first item to the output list, use int() get an integer

def ip_range(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = [] 
   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))    
   return ip_range

def find_ip_command():
    cmdgetcpu="arp-scan 192.168.1.0/24 >used_ip.txt"
    hostcpuutil=subprocess.check_output(cmdgetcpu,shell=True)


def find_ip():
    global iprange
    global ip_list
    find_ip_command()
    read_file()
    iprange = ip_range("192.168.1.2", "192.168.1.254")
    ip_not_used = [x for x in iprange if x not in ip_list]
    random.shuffle(ip_not_used)
    length_ip = sys.argv[1]
    print length_ip
    ip_foruser = ip_not_used[0:int(length_ip)]
    print ip_foruser

find_ip() 
