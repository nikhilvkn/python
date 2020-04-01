from inception import InceptionTools, Server, Service
import argparse
import sys


def main():
	'''Gather inception server details'''

	parse = argparse.ArgumentParser()
	parse.add_argument('-d','--dc', help=': name of an inception datacenter', metavar='')
	parse.add_argument('-e','--env', help=': environment in a datacenter', metavar='')
	parse.add_argument('-l','--listenv', help=': datacenter name to get available environments', metavar='')
	parse.add_argument('-s','--service', nargs='+', type=str, help=': service to query for its servers', metavar='')
	parse_arguments = parse.parse_args()

	if parse_arguments.listenv:
		inception_request = InceptionTools(parse_arguments.listenv)
		for content in inception_request.environment():
			print(content)
		sys.exit()

	if parse_arguments.service:
		service_data = parse_arguments.service[0].split(',')
		inception_request = Service(parse_arguments.dc, parse_arguments.env)
		all_service = inception_request.specific_service()
		for content in service_data:
			if content not in all_service:
				print(f'''FileNotFound Exception: Service {content} not found in {parse_arguments.env} environment.
Please re-check service name or use service option [--help]''')
				sys.exit()
		inception_request = Server(parse_arguments.dc, parse_arguments.env, service_data)
		for content in inception_request.specific_service():
			print(content)
		sys.exit()

	if parse_arguments.dc:
		if bool(parse_arguments.dc) ^ bool(parse_arguments.env):
			inception_request = Server(parse_arguments.dc)
			for content in inception_request.all_server():
				print(content)
		else:
			inception_request = Server(parse_arguments.dc, parse_arguments.env)
			for content in inception_request.specific_server():
				print(content)
	else:
		print('''SyntaxError: Insuficient arguments
Check --help option to know more''')


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass