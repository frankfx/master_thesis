#!/bin/bash
if [ $# -ge 2 ]; then
	# rmi connection
	java -jar jmxterm-1.0-alpha-4-uber.jar -l service:jmx:rmi:/// ...
else
	echo "for rmi type : ./run.sh <host> <port>"
	p=$(jps | grep MainServer | cut -d ' ' -f 1)

	if [  -z "$p" ] 
	then
		exit 0
	fi	
	...
	sed -i '1i open '"$p" script.txt
	java -jar jmxterm-1.0-alpha-4-uber.jar -n -i script.txt -o output.txt
	...
fi











