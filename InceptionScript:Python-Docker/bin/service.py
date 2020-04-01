from inception import InceptionTools, Service
import argparse
import sys


def main():
	'''Gather inception services'''

	parse = argparse.ArgumentParser()
	parse.add_argument('-d','--dc', help=': name of an inception datacenter', metavar='')
	parse.add_argument('-e','--env', help=': environment in a datacenter', metavar='')
	parse.add_argument('-l','--listenv', help=': datacenter name to get available environments', metavar='')
	parse_arguments = parse.parse_args()

	if parse_arguments.listenv:
		inception_request = InceptionTools(parse_arguments.listenv)
		for content in inception_request.environment():
			print(content)
		sys.exit()

	if parse_arguments.dc:
		if bool(parse_arguments.dc) ^ bool(parse_arguments.env):
			inception_request = Service(parse_arguments.dc)
			for content in inception_request.all_service():
				print(content)
		else:
			inception_request = Service(parse_arguments.dc, parse_arguments.env)
			for content in inception_request.specific_service():
				print(content)
	else:
		print('''SyntaxError: Insuficient arguments
Check --help option to know more''')


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		pass