import services
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
diskcommand = "df -h | awk {'print $5" "$6'} | sed 1d | grep -v '/usr'"
homeDir = os.getenv("HOME")
spaceFile = os.path.join(homeDir, 'core-space')
spaceContents = []

def diskCheck():
	''' main function to handle disk check '''

	for dc in datacenters:
		datacenterContents = services.parseData(dc)
		servers = serverinfo(datacenterContents, environment)

		# get the space details for core servers
		spaceData = checkSpace(servers)

		# print the space usage
		spaceDisplay(spaceData, dc)

class connect_to:
	''' class definition to do server specific operations '''

	def __init__(self, server_name, username, key):
		self.ssh = paramiko.SSHClient()
		self.ssh.load_system_host_keys()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(hostname=server_name, username=username, key_filename=key)

	def run_command(self, command):
		if(self.ssh):
			stdin, stdout, stderr = self.ssh.exec_command(command)
			return stdout.read()
		else:
			print('Connection is not opened')


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
		with open(spaceFile, 'a+') as contents:
			contents.write('''
[DISK CHECK: > 90] {} datacenter:
---------------------------------
'''.format(datacenter))
		for content in spaceData:
			with open(spaceFile, 'a+') as contents:
				contents.write(content+'\n')
	else:

		with open(spaceFile, 'a+') as contents:
			contents.write('''
[DISK CHECK: > 90] {} datacenter:
---------------------------------
Disk space seems proper!
'''.format(datacenter))
	

def checkSpace(servers):
	''' function to do the logic in space decision '''

	sizelist = []
	for server in servers:
		ssh_to = connect_to(server, username, key)
		spaceResult = ssh_to.run_command(diskcommand).decode('utf8').strip().split('\n')
		spaceData = dict([x.split('%') for x in spaceResult])

		for percentage, partition in spaceData.items():
			if int(percentage) >= 90:
				sizelist.append('''SERVER: {}		PRESENT SIZE: {}	PARTITION: {}'''.format(server,percentage,partition))
			else:
				pass

	return sizelist
	

if __name__ == '__main__':

	try:
		if spaceFile:
			os.remove(spaceFile)
			diskCheck()
	except FileNotFoundError:
			diskCheck()	
	except KeyboardInterrupt:
		pass