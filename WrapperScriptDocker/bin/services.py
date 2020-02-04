import argparse
import requests
import json
import sys
import os

example_text = '''
Example:
docker run -it --rm --net host docker.xxxx.com/nnarayanan/inception-scripts listall-services  -d xxxx
docker run -it --rm --net host docker.xxxx.com/nnarayanan/inception-scripts listall-services  -l xxxx
docker run -it --rm --net host docker.xxxx.com/nnarayanan/inception-scripts listall-services  -d xxxx -e core
'''

def main():
	# Main module with passed arguments

	parse = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
	parse.add_argument('-d','--dc', help=': name of an inception datacenter', metavar='')
	parse.add_argument('-l','--listenv', help=': datacenter name to get available environments', metavar='')
	parse.add_argument('-e','--env', help=': environment in a datacenter', metavar='')
	parse_arguments = parse.parse_args()

	if parse_arguments.listenv:
		allEnv = allEnvironments(parse_arguments.listenv)
		printResult(allEnv)

	if parse_arguments.dc:
		if bool(parse_arguments.dc) ^ bool(parse_arguments.env):
			allService = allServices(parse_arguments.dc)
			printResult(allService)
		else:
			specificService = specificServices(parse_arguments.dc, parse_arguments.env)
			printResult(specificService)	
	
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

def allEnvironments(datacenter):
	# Gather all environments in a given datacenter

	env_result = []
	data = parseData(datacenter)
	for elements in data['dynconfigMonitoringServerUrls']:
		env_result.append(elements['environment'])
	sorted_result = get_unique(env_result)
	return sorted_result

def allServices(datacenter):
	# Gather details about all service in a datacenter

	allservices = []
	data = parseData(datacenter)
	for elements in data['dynconfigMonitoringServerUrls']:
		for values in elements['url']:
			allservices.append(values['container'])
	sorted_result = get_unique(allservices)
	return sorted_result

def specificServices(datacenter, environment):
	# Gather details about specific services in a datacenter

	services = []
	data = parseData(datacenter)
	for elements in data['dynconfigMonitoringServerUrls']:
		for values in elements['url']:
			if elements['environment'] == environment:
				services.append(values['container'])
	sorted_result = get_unique(services)
	return sorted_result

def printResult(message):
	# Print out contents in a list and exit out
	for contents in message:
		print(contents)
	sys.exit()
			
def get_unique(my_result):
	# Function to get the unique out of given
	return list(set(my_result))


if __name__ == '__main__':
	# Main program to manage service in an Inception Datacenter

	try:
		main()
	except KeyboardInterrupt:
		pass