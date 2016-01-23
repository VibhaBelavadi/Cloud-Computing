#!/bin/bash

nodename="$1"
nodeid="$2"
memory="$3"
vcpu="$4"
imgfilepath="$5"
configxmlfilepath="$6"
hostip="$7"

imgfilename=$( basename "$5" )
xmlfilename=$( basename "$6" )
uuid=$(uuidgen)
macaddr=$(python /home/node4_a1/GenerateMac.py)
maxmemory=`expr $3 \\* 2`
masterip="192.168.1.40"
mkdir -m 777 "/home/guestdata/$nodename"

newimgfilepathforxml="\/home\/guestdata\/$nodename\/$nodename\.qcow2"
newimgfilepath="/home/guestdata/$nodename/$nodename.qcow2"
cp $imgfilepath $newimgfilepath
xmlfilepath="/home/guestdata/$nodename/$xmlfilename"
cp $configxmlfilepath $xmlfilepath

sed -i -e "s/VM_ID/$nodeid/g" $xmlfilepath
sed -i -e "s/VM_NAME/$nodename/g" $xmlfilepath
sed -i -e "s/VM_UUID/$uuid/g" $xmlfilepath
sed -i -e "s/VM_CURRMEM/$memory/g" $xmlfilepath
sed -i -e "s/VM_MAXMEM/$maxmemory/g" $xmlfilepath
sed -i -e "s/VM_VCPU/$vcpu/g" $xmlfilepath
sed -i -e "s/VM_MAC_ADDRESS/$macaddr/g" $xmlfilepath
sed -i -e "s/VM_SOURCEIMG/$newimgfilepathforxml/g" $xmlfilepath

ssh root@$hostip virsh create $xmlfilepath

