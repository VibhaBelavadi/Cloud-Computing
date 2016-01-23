vmname="$1"
hostipaddr="$2"
vmxmlfile="/home/guestdata/$vmname/Config_WithTokens.xml"
targetloc="/home/node4_a1/define/$vmname.xml"
scp $vmxmlfile root@$hostipaddr:$targetloc
ssh root@$hostipaddr virsh define $targetloc
ssh root@$hostipaddr virsh shutdown $vmname
sleep 10
ssh root@$hostipaddr virsh start $vmname
ssh root@$hostipaddr rm -rf $targetloc
echo $?              
