#!/bin/bash

vmname="$1"
sourcehost="$2"
targethost="$3"
ssh root@$sourcehost virsh migrate --live $vmname qemu+ssh://$targethost/system --unsafe
echo $?
