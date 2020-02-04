from collections import Counter
import sys
import requests
import json
import argparse

example_text = '''
Example:
docker run -it --rm --net host docker.xxxx.com/nnarayanan/inception-scripts services-lt-3  -l xxxx
docker run -it --rm --net host docker.xxxx.com/nnarayanan/inception-scripts services-lt-3  -d xxxx -e production

'''
env_list = []

def main():

	parse = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter, prog="services_lt_3.py")
	parse.add_argument('-d','--dc', help=": inception datacenter name", metavar='')
	parse.add_argument('-e','--env', help=": give environment of your choice", metavar='')
	parse.add_argument('-l','--listenv', help=": helps you find environments in a datacenter", metavar='')
	parse_arguments = parse.parse_args()

	if parse_arguments.listenv:
		checkEnv(parse_arguments.listenv)

	elif bool(parse_arguments.dc) ^ bool(parse_arguments.env):
		parse.error('''--dc and --env must be given together
  				Use --help option to know more\n''')
	else:
		checkInfo(parse_arguments.dc, parse_arguments.env)


def get_unique(my_list):

    return list(set(my_list))

def get_value(info):

	try:
		responsedata = requests.get('http://dynconfig.'+str(info)+'.tivo.com:50000/MonitoringUrls')
		fulldata = json.loads(responsedata.text)
		return fulldata
	except Exception as e:
		print('\nConnection timed out. Please cross check provided values\n')
		sys.exit()

def checkEnv(environment):

	work_fulldata = get_value(environment)
	for elements in work_fulldata['dynconfigMonitoringServerUrls']:
		env_list.append(elements['environment'])
	sorted_list = get_unique(env_list)
	for items in sorted_list:
		print(items)
	sys.exit()

def populateEnvironment(datacenter, environment):

	data = get_value(datacenter)
	environment = []
	for elements in data['dynconfigMonitoringServerUrls']:
			environment.append(elements['environment'])
	sortedEnvironment = get_unique(environment)
	return sortedEnvironment

def availableCheck(data, environment):

	if environment in data:
		pass
	else:
		print('\nGiven environment {} is not present in this datacenter\n'.format(environment))
		sys.exit()


def checkInfo(datacenter, environment):

	count = {}
	service_list = []
	avaliableEnvironment = populateEnvironment(datacenter, environment)
	availableCheck(avaliableEnvironment, environment)
	work_fulldata = get_value(datacenter)
	for elements in work_fulldata['dynconfigMonitoringServerUrls']:
		for values in elements['url']:
			if elements['environment'] == environment:
				service_list.append(values['container'])
	count = Counter(service_list)
	counter = 0
	for key, value in count.items():
		if value < 3:
			counter += 1
			print(key +' : '+ str(value))
	if counter == 0:
		print("\n All services have 3 or more instances\n")
	sys.exit()

if __name__ == '__main__':
	try:
		if sys.argv[1:]:
			main()
		else:
			print('\nExcept ateast one argument. Please check --help option\n')
	except KeyboardInterrupt:
		pass