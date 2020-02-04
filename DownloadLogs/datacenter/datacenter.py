import requests
import paramiko
import socket
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
		self.sftpclient = self.ssh.open_sftp()

	def run_command(self, command):
		if(self.ssh):
			stdin, stdout, stderr = self.ssh.exec_command(command)
			return stdout.read()
		else:
			print('Connection is not opened')

	def exists(self, path):
		try:
			self.sftpclient.stat(path)
		except FileNotFoundError:
			return False
		else:
			return True

def parseData(environment):
	''' function to gather a specific datacenter details as json'''

	try:
		responsedata = requests.get('http://dynconfig.'+environment+'.tivo.com:50000/MonitoringUrls')
		fulldata = json.loads(responsedata.text)
		return fulldata
	except Exception as e:
		print("\nConnection timed out. Please check your network settings\n")
		sys.exit()

def allServers(datacenter):
	''' function to gather all servers in a datacenter '''

	servers = []
	data = parseData(datacenter)
	for server in data['dynconfigMonitoringServerUrls']:
		servers.append(server['server'])
	return servers

def specificServers(datacenter, environment):
	# Gather servers specific to an environment

	servers = []
	data = parseData(datacenter)
	for elements in data['dynconfigMonitoringServerUrls']:
		if elements['environment'] == environment:
			servers.append(elements['server'])
	return servers


def specificServices(datacenter, environment):
	''' function to gather all services based on environment '''

	services = []
	data = parseData(datacenter)
	for elements in data['dynconfigMonitoringServerUrls']:
		for values in elements['url']:
			if elements['environment'] == environment:
				services.append(values['container'])
	sorted_result = get_unique(services)
	return sorted_result


def allServices(datacenter):
	''' function to gather all services in a datacenter '''

	allservices = []
	data = parseData(datacenter)
	for elements in data['dynconfigMonitoringServerUrls']:
		for values in elements['url']:
			allservices.append(values['container'])
	sorted_result = get_unique(allservices)
	return sorted_result


def checkConnection(server):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((server, 22))
      s.shutdown(2)
      return True
   except:
      return False


def get_unique(my_result):
	''' function to return unique list '''

	return list(set(my_result))


if __name__ == '__main__':

	try:
		datacenter()
	except KeyboardInterrupt:
		pass