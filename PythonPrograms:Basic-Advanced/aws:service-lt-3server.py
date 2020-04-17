import sys, requests, json, argparse
from collections import Counter

env_list = []

example_text = '''
Example:
'''+str(sys.argv[0])+ ''' --listenv tpc1
'''+str(sys.argv[0])+ ''' --dc tpc1 --env production
'''
parse = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
parse.add_argument("--dc", help="give datacenter name")
parse.add_argument("--env", help="give environment of your choice")
parse.add_argument("--listenv", help="helps you find environments in a datacenter")
parse_arguments = parse.parse_args()

def get_unique(my_list):
	return list(set(my_list))

def get_value(info):
	try:
		responsedata = requests.get('http://dynconfig.'+str(info)+'.tivo.com:50000/MonitoringUrls')
		fulldata = json.loads(responsedata.text)
		return fulldata
	except Exception as e:
		print("\nConnection timed out. Please check your network settings\n")
		sys.exit()

if parse_arguments.listenv:
	work_fulldata = get_value(parse_arguments.listenv)
	for elements in work_fulldata['dynconfigMonitoringServerUrls']:
		env_list.append(elements['environment'])
	sorted_list = get_unique(env_list)
	for items in sorted_list:
		print(items)
	sys.exit()

service_list = []

if  parse_arguments.dc and len(sys.argv) == 5:
	work_fulldata = get_value(parse_arguments.dc)
	for elements in work_fulldata['dynconfigMonitoringServerUrls']:
		for values in elements['url']:
			if elements['environment'] == str(parse_arguments.env):
				service_list.append(values['container'])
else:
	print("\nPlease check help option\n")

# Print the services less than in 3 instances
count = Counter(service_list)	#Initialising Counter class with argument as service_list. Output will be a dictionary, which is stored in count
counter = 0
for key, value in count.items():
	if value < 3:
		counter += 1
		print(key +' : '+ str(value))
if counter == 0:
	print("\n All services have 3 or more instances\n")

#END
