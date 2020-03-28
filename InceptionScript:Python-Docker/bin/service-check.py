from paramiko.auth_handler import AuthenticationException, SSHException
from paramiko import SSHClient, AutoAddPolicy, RSAKey
import inception
import requests
import argparse
import socket
import json
import sys
import os


KEY = 'xxx'
USERNAME = 'xxx'
DOCKER_COMMAND = 'docker ps -a --format "table {{.Names}}\t{{.Status}}"'
ERROR_WORDS = ['DOWN','NOT RUNNING','REBALANCING']


class RemoteConnect:
	'''Class to peform SSH operations'''

	def __init__(self, server_name):
		try:
			self.ssh = SSHClient()
			self.ssh.load_system_host_keys()
			self.ssh.set_missing_host_key_policy(AutoAddPolicy())
			self.ssh.connect(hostname=server_name, 
							 username=USERNAME, 
							 key_filename=KEY, 
							 timeout=20)
		except AuthenticationException:
			print('Authentication Failed: Please check your network/ssh key')
		except socket.timeout:
			print('SSHConnectionError: Failed to connect server\n')
			sys.exit()

	def run_command(self, command):
		if(self.ssh):
			stdin, stdout, stderr = self.ssh.exec_command(command)
			return stdout.read()
		else:
			print('Connection is not opened')


class ServiceCheck():
	'''Gathering endpoint status for inception service'''

	def __init__(self, service_name, dc_data, environment):
		self.service_name = service_name
		self.dc_data = dc_data
		self.environment = environment

	def service_url(self):
		service_url = []
		for element in self.dc_data['dynconfigMonitoringServerUrls']:
			for content in element['url']:
				if element['environment'] == self.environment and content['container'] == self.service_name:
					service_url.append(content['url'])
		return service_url


class ServicePrint(ServiceCheck):
	'''Handle print method efficiently'''

	def __init__(self, service_name, dc_data, environment):
		super().__init__(service_name, dc_data, environment)

	def gather_status(self, data):
		for word in ERROR_WORDS:
			if word not in str(data):
				continue
			else:
				print('Service Status   : NOT READY')
				return
		print('Service Status   : UP')

	def info_print(self, data):
		if data:
			try:
				print('Application Name : '+data['app']['name'])
				print('Build Number     : '+data['build']['number'])
				print('Build Time       : '+data['build']['time'])
			except KeyError:
				pass

	def endpoint_print(self, data):
		if data:
			try:
				print('Service Status   : '+data['status'])	
			except (KeyError, TypeError):
				self.gather_status(data)

	def endpoint_check(self, url, check):
		try:
			responsedata = requests.get(url+'/'+check)
			full_data = json.loads(responsedata.text)
			self.info_print(full_data) if check == 'info' else self.endpoint_print(full_data)

		except json.decoder.JSONDecodeError:
			code_data = os.popen('curl -ks '+url+'/'+check).read()
			self.gather_status(code_data)
		except requests.exceptions.ConnectionError:
			print('Exception: Upgrade in progress')


def endpoint_check(service_data, dc_data, env):
	'''Module to print endpoint status'''
	
	for service in service_data:
		inception_request = ServicePrint(service, dc_data, env)
		service_url = inception_request.service_url()
		print('\n-----------------------SERVICE NAME: '+service+'-----------------------\n')
		for url in service_url:
			instance_name = url[7:-12]
			print('-------INSTANCE NAME: '+instance_name+'\n')
			ssh_to = RemoteConnect(instance_name)
			common_url = url[:-6]
			print('/INFO FOR: '+service)
			inception_request.endpoint_check(common_url, 'info')
			print('/CHECK FOR: '+service)
			inception_request.endpoint_check(common_url, 'check')
			print('/HEALTH FOR: '+service)
			inception_request.endpoint_check(common_url, 'health')
			print('CONTAINER STATUS:')
			container = ssh_to.run_command(DOCKER_COMMAND +'| grep '+service)
			if not container:
				print('RunTimeException: Container {} is not running'.format(service))
			else:
				print(container.decode('utf8').strip('\n'))
			print('\n')


def errorout(service, environment):
	print('''
	Service {} is not available in environment {}
	Use --listenv to see the available environments
	Use --help to see all options\n'''.format(service, environment))
	sys.exit()


def main():
	'''Program to check service status'''

	parse = argparse.ArgumentParser()
	parse.add_argument('-d','--dc', help=': inception datacenter name', metavar='')
	parse.add_argument('-e','--env', help=': give environment of your choice', metavar='')
	parse.add_argument('-l','--listenv', help=': helps you find environments in a datacenter', metavar='')
	parse.add_argument('-s','--service', nargs='+', type=str, help=': services to gather details', metavar='')
	parse_arguments = parse.parse_args()

	if parse_arguments.listenv:
		inception_request = inception.InceptionTools(parse_arguments.listenv)
		for content in inception_request.environment():
			print(content)
		sys.exit()

	if parse_arguments.service:
		'''Cross checking defined services with environment services'''

		service_data = parse_arguments.service[0].split(',')
		inception_request = inception.Service(parse_arguments.dc, parse_arguments.env)
		all_service = inception_request.all_service()
		for service in service_data:
			if service not in all_service:
				errorout(service, parse_arguments.env)
				
	if bool(parse_arguments.dc) ^ bool(parse_arguments.service):
			parse.error('''-d -e & -s must be given together
		  Use --help option to know more''')
	else:
		inception_request = inception.InceptionTools(parse_arguments.dc)
		dc_data = inception_request.dc_data()
		endpoint_check(service_data, dc_data, parse_arguments.env)


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass