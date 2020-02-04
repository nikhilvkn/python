from datacenter import datacenter
import argparse
import paramiko
import json
import sys
import os

# Declaring necessary variables to use:
environment = 'xxxx'
datacenters = ['xxxx']
key = 'xxxx'
username = 'xxxx'

diskcommand = "df -h | awk {'print $5" "$6'} | sed 1d"

def diskCheck():
	''' main function to handle disk check '''

	for dc in datacenters:
		datacenterContents = datacenter.parseData(dc)
		servers = serverinfo(datacenterContents, environment)
		
		# get the space details for core servers
		spaceData = checkSpace(servers)

		# print the space usage
		spaceDisplay(spaceData, dc)


def serverinfo(datacenterContents, environment):
	''' function helps to gather server's based on given datacenter '''
	
	server = []
	for elements in datacenterContents['dynconfigMonitoringServerUrls']:
		if elements['environment'] == environment:
			server.append(elements['server'])

	return server


def spaceDisplay(spaceData, datacenter):
	''' function to print space details '''

	if spaceData:
		print('''
[DISK CHECK > 90:] {} datacenter:
---------------------------------'''.format(datacenter))
		for contents in spaceData:
			print(contents)
	else:
		print('''
[DISK CHECK > 90:] {} datacenter:
---------------------------------
Disk space seems proper!'''.format(datacenter))


def checkSpace(servers):
	''' function to do the logic in space decision '''

	sizelist = []
	for server in servers:
		ssh_to = datacenter.connect_to(server, username, key)
		spaceResult = ssh_to.run_command(diskcommand).decode('utf8').strip().split('\n')
		spaceData = dict([x.split('%') for x in spaceResult])

		for percentage, partition in spaceData.items():
			counter = 0
			if int(percentage) >= 90:
				sizelist.append('''SERVER: {}		PRESENT SIZE: {}	PARTITION: {}'''.format(server,percentage,partition))
			else:
				pass

	return sizelist
	

if __name__ == '__main__':

	try:
		diskCheck()
	except KeyboardInterrupt:
		pass