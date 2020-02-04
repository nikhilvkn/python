import argparse
import requests
import services
import json
import sys
import os

example_text = '''
Example:
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts listall-servers  -l xxx
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts listall-servers  -d xxx
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts listall-servers  -d xxx -e production
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts listall-servers  -d xxx -e production -s voice
'''

def main():
	# Main program with arguments

	parse = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
	parse.add_argument('-d','--dc', help=': list all servers in a datacenter', metavar='')
	parse.add_argument('-e','--env', help=': environment in a datacenter', metavar='')
	parse.add_argument('-l','--listenv', help=': list all available environments in a datacenter', metavar='')
	parse.add_argument('-s','--service', nargs='+', type=str, help=': service to query for its servers', metavar='')
	parse_arguments = parse.parse_args()

	if parse_arguments.listenv:
		allEnv = services.allEnvironments(parse_arguments.listenv)
		services.printResult(allEnv)

	if parse_arguments.service:
		servicedata = parse_arguments.service[0].split(',')
		serviceSpecific(parse_arguments.dc, parse_arguments.env, servicedata)

	if parse_arguments.dc:
		if bool(parse_arguments.dc) ^ bool(parse_arguments.env):
			allServer = allServers(parse_arguments.dc)
			services.printResult(allServer)
		else:
			specificServer = specificServers(parse_arguments.dc, parse_arguments.env)
			services.printResult(specificServer)
	else:
		print('''\nError: InsuficientArguments:
Check --help option to know more\n''')

def parseData(environment):
	# Gather whole data of a dc using dynconfig

	try:
		responsedata = requests.get('http://dynconfig.'+environment+'.tivo.com:50000/MonitoringUrls')
		fulldata = json.loads(responsedata.text)
		return fulldata
	except Exception as e:
		print("\nConnection timed out. Please check your network settings\n")
		sys.exit()

def allServers(datacenter):
	# Gather all servers in a datacenter

	data = parseData(datacenter)
	for server in data['dynconfigMonitoringServerUrls']:
		servers.append(server['server'])
	return servers

def specificServers(datacenter, environment):
	# Gather servers specific to an environment

	data = parseData(datacenter)
	for elements in data['dynconfigMonitoringServerUrls']:
		if elements['environment'] == environment:
			servers.append(elements['server'])
	return servers

def serviceSpecific(datacenter, environment, sdata):
	# Gather servers based on services

	data = parseData(datacenter)
	verifyInput(environment, data, sdata)

	for services in sdata:
		print('\nSERVICE: {}'.format(services))
		print('-------------------')
		for elements in data['dynconfigMonitoringServerUrls']:
			for contents in elements['url']:
				if elements['environment'] == environment and contents['container'] == services:
					print(elements['server'])
				else:
					pass
	sys.exit()

def verifyInput(environment, data, service):
	# Verify the imput provided to proceed further

	container = []
	for elements in data['dynconfigMonitoringServerUrls']:
		for contents in elements['url']:
			if elements['environment'] == environment:
				container.append(contents['container'])
	for elements in service:
		if elements not in container:
			print('''\nservice {} is not found in environment {}.
please recheck service name or use listall-services option [--help]\n'''.format(elements,environment))
			sys.exit()
		else:
			pass


if __name__ == '__main__':
	# Main program 
	try:
		servers = []
		main()
	except KeyboardInterrupt:
		pass