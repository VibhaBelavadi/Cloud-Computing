#!/bin/bash/
#Root privileges

#Make it passwordless ssh
#sshpass -pcloud123 ssh-copy-id root@$1 

#get into the ipaddress
ssh root@$1 "

#install epel rpm package
rpm -Uvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
#to check the available repository
#yum repolist
#yum --disablerepo="*" --enablerepo="epel" list available

#install ganglia
yum install ganglia.x86_64 -y
#install ganglia_gmond
yum install ganglia-gmond.x86_64 -y

#yum install ganglia-gmetad.x86_64 -y #install ganglia_metad, required only in host
#yum install ganglia-web.x86_64 #install ganglia_web, required only in host

"
scp /etc/ganglia/gmond.conf root@$1:/etc/ganglia

ssh root@$1 service gmond restart
