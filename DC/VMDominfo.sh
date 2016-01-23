#!/bin/bash
#Read the dominfo and get VCPUs count and the current memory assignment in the VM_DomInfo.txt file

echo "$1" > virtNm.txt

scp virtNm.txt root@$2:/home

rm -f virtNm.txt  

ssh -n root@$2 '

	virtN=$(head -n1 /home/virtNm.txt)
	
	VCPU=$( virsh dominfo $virtN | sed '6!d' | egrep -o "[0-9]+" )
	
	Mem_used=$( virsh dominfo $virtN | sed '9!d' | egrep -o "[0-9]+" )

	Mem_max=$(virsh dominfo $virtN | sed '8!d' | egrep -o "[0-9]+" )

	echo "$VCPU|$Mem_used|$Mem_max"

'
