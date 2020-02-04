import paramiko
import requests
import argparse
import json
import sys
import os

example_text = '''
Example:
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts service-check -l xxxx
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts service-check -d xxxx -e core -s zookeeper,haproxy

'''
key = 'xxxx'
username = 'xxxx'
docker_command = 'docker ps -a --format "table {{.Names}}\t{{.Status}}"'

def inceptionCheck():
	
	parse = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
	parse.add_argument('-d','--dc', help=': inception datacenter name', metavar='')
	parse.add_argument('-e','--env', help=': give environment of your choice', metavar='')
	parse.add_argument('-l','--listenv', help=': helps you find environments in a datacenter', metavar='')
	parse.add_argument('-s','--service', nargs='+', type=str, help=': services to gather details', metavar='')
	parse_arguments = parse.parse_args()
	
	if parse_arguments.service:
		servicedata = parse_arguments.service[0].split(',')

	if parse_arguments.listenv:
		finalresult, envresult = ([], [])
		
		datacenterContents = datacenterDetails(parse_arguments.listenv)
		for elements in datacenterContents['dynconfigMonitoringServerUrls']:
			envresult.append(elements['environment'])
		sortedresult = getUnique(envresult)
		for items in sortedresult:
			print(items)
		sys.exit()

	if bool(parse_arguments.dc) ^ bool(parse_arguments.service):
			parse.error('''-d -e & -s must be given together
		  Use --help option to know more\n''')
	else:
		datacenterContents = datacenterDetails(parse_arguments.dc)
		isservicePresent(parse_arguments.dc, parse_arguments.env, servicedata)

		workon(servicedata, datacenterContents, parse_arguments.env)

def datacenterDetails(datacenter):

	try:
		responsedata = requests.get('http://dynconfig.'+datacenter+'.tivo.com:50000/MonitoringUrls')
		fulldata = json.loads(responsedata.text)
		return fulldata
	except Exception as e:
		print("\nConnection timed out. Please check your network settings\n")
		sys.exit()


def getUnique(my_result):
	return list(set(my_result))

def errorout(service, environment):
	print('''
	Service {} is not available in environment {}
	Use --listenv to see the available environments
	Use --help to see all options\n'''.format(service, environment))
	sys.exit()

def isservicePresent(datacenter, environment, definedservices):

	data = datacenterDetails(datacenter)
	services = []
	for elements in data['dynconfigMonitoringServerUrls']:
		for values in elements['url']:
			if elements['environment'] == environment:
				services.append(values['container'])
	sortedServices = getUnique(services)
	
	for services in definedservices:
		if services not in sortedServices:
			errorout(services, environment)
		else:
			pass


class connect_to:

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


def workon(definedservices, datacenterContents, environment):
	
	for contents in definedservices:
		urlresult = []
		for elements in datacenterContents['dynconfigMonitoringServerUrls']:
			for values in elements['url']:		
				if elements['environment'] == environment and values['container'] == contents:
					urlresult.append(values['url'])

		print('\n-----------------------SERVICE NAME: '+contents+'-----------------------\n')
		for urls in urlresult:
			name = urls[7:-12]
			print('-------INSTANCE NAME: '+name+'\n')
			finalurls = urls[:-6]
			print('/INFO FOR: '+contents)
			serviceInfo(finalurls)
			print('/CHECK FOR: '+contents)
			serviceCheck(finalurls)
			print('/HEALTH FOR: '+contents)
			serviceHealth(finalurls)
			print('CONTAINER STATUS:')
			ssh_to = connect_to(name, username, key)
			container = ssh_to.run_command(docker_command +'| grep '+contents)
			if not container:
				print('Container {} is getting restarted'.format(contents))
			else:
				print(container.decode('utf8').strip('\n'))
			print('\n')


def gatherServicedata(dataUrl, check):

	try:
		responsedata = requests.get(dataUrl+'/'+check)
		fulldata = json.loads(responsedata.text)
		return fulldata

	except json.decoder.JSONDecodeError:
		os.system('curl -ks '+dataUrl+'/'+check)
	except requests.exceptions.ConnectionError:
		print('ConnectionError: Unable to connect to service')
		pass

def serviceInfo(serviceUrl):

	requirement = 'info'
	data = gatherServicedata(serviceUrl, requirement)
	if data:
		try:
			print('Application Name : '+data['app']['name'])
			print('Build Number     : '+data['build']['number'])
			print('Build Time       : '+data['build']['time'])
		except KeyError:
			pass
	else:
		pass

def serviceCheck(serviceUrl):

	requirement = 'check'
	data = gatherServicedata(serviceUrl, requirement)
	if data:
		try:
			print('Service Status   : '+data['status'])
		except (KeyError, TypeError):
			print('Service Status   : '+str(data))
	else:
		pass

def serviceHealth(serviceUrl):

	requirement = 'health'
	data = gatherServicedata(serviceUrl, requirement)
	if data:
		try:
			print('Service Status   : '+data['status'])
		except (TypeError, KeyError):
			print('Service Status   : '+str(data))
	else:
		pass


if __name__ == '__main__':

	try:
		inceptionCheck()

	except KeyboardInterrupt:
		pass

else:
	print("\nPlease check help option\n")