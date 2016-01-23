#!/usr/bin/python
import  sys
from VMEditDefine import editParameterInXML
from VMEditDefine import defineVM

def main():
	vmip=sys.argv[1]
	param=sys.argv[2]
	value=sys.argv[3]
	editParameterInXML(vmip,param,value)
    	defineVM(vmip)
	
if __name__=="__main__":
	main()
