import requests
import paramiko
import json
import sys
import os

def datacenter():

	# pass the program to next functions
	pass

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


def parseData(environment):
	# Gather whole data of a dc using dynconfig

	try:
		responsedata = requests.get('http://dynconfig.'+environment+'.tivo.com:50000/MonitoringUrls')
		fulldata = json.loads(responsedata.text)
		return fulldata
	except Exception as e:
		print("\nConnection timed out. Please check your network settings\n")
		sys.exit()

if __name__ == '__main__':

	try:
		datacenter()
	except KeyboardInterrupt:
		pass