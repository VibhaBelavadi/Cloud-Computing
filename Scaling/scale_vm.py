#!/usr/bin/python
import os
import subprocess
#import parmiko

#ssh = paramiko.SSHClient()
#ssh.connect('192.168.1.22', username=root, password=cloud123)
#ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(ls)
createCmd = "ssh root@192.168.1.22 sh scale_machine.sh"
subprocess.check_call(createCmd,shell=True)
