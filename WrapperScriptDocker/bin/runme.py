#!/usr/bin/python

import os
import sys
import argparse

def main(arguments):

	#Co-relate to the command and corresponding scripts to trigger
	scripts = {
			'service-check' : '/home/xxx/bin/service-check.py',
			'service-lt-3' : '/home/xxx/bin/services-lt-3.py',
			'listall-servers' : '/home/xxx/bin/servers.py',
			'listall-services' : '/home/xxx/bin/services.py',
		}

	example_text = '''
Example:
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts --help
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts service-check --help
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts service-check -d tpab1 -e core -s zookeeper,haproxy
docker run -it --rm --net host docker.xxx.com/nnarayanan/inception-scripts listall-servers -d tpc1
'''
	parse = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
	parse.add_argument('command', 
						help='command to query inception\n: {}'.format(', '.join(sorted(scripts.keys()))))
	parse.add_argument('args', nargs=argparse.REMAINDER,
						help='The arguments to the command')
	parse_arguments = parse.parse_args(arguments)

	if parse_arguments.command not in scripts:
		print('These are the available scripts to run:')
		print('\n'.join(sorted(scripts.keys())))
	else:
	 	os.execv(scripts.get(parse_arguments.command), [scripts.get(parse_arguments.command)] + parse_arguments.args)

if __name__ == '__main__':
	try:
		main(sys.argv[1:])
	except KeyboardInterrupt:
		pass








