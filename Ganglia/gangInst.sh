#!/bin/bash/
#Root privileges

#Make it passwordless ssh
sshpass -pcloud123 ssh-copy-id root@$1 

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

sed -i -e 's/name = "unspecified"/name = "Cloud123"/' -e 's/name = "Ganglia Test Setup"/name = "Cloud123"/' -e 's/bind = 239.2.11.71/#bind = 239.2.11.71/' /etc/ganglia/gmond.conf

sed '0,/mcast_join = 239.2.11.71/s//host = 192.168.1.40/' /etc/ganglia/gmond.conf

service gmond start

"
