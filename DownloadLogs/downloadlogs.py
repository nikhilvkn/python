from datacenter import datacenter
import subprocess
import argparse
import paramiko
import tarfile
import shutil
import sys
import os

# Global variable declaration

homeDir = os.getenv("HOME")
scpDir = 'LogDirectory'
downloadDir = os.path.join(homeDir,scpDir)


def checkPath(path, serverdata):
	''' function to check if path/log file exists '''

	location = []
	ssh_to = datacenter.connect_to(serverdata, username = parse_arguments.user, key = key)
	if ssh_to.exists(path) == True:
		log = parse_arguments.file[0].split(',')
		[location.append(os.path.join(path,elements)) for elements in log]
		logdata = [location[index] for index, value in enumerate(list(map(ssh_to.exists, location))) if value == False]
		if logdata:
			print('ERROR: FileNotFound: {} cannot be found'.format(logdata))
		else:
			return location
	else:
		print('ERROR: PathNotExists: {} does not exists'.format(path))
		sys.exit()


def connectionCheck(serverdata):
	''' function to check connection to the given servers '''

	connection = list(map(datacenter.checkConnection, serverdata))
	notaccessible = [(server) for server,value in list(zip(serverdata,connection)) if value == False]
	if notaccessible:
		print('ERROR: ServerConnection: Unable to connect {}'.format(notaccessible))
		sys.exit()
	else:
		return checkPath(parse_arguments.path, serverdata[0])


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


@run_once
def checkDir(dataDir):
	''' applying a decorator function to check directory '''

	if os.path.exists(dataDir) and os.path.isdir(dataDir):
		if os.listdir(dataDir):
			shutil.rmtree(dataDir, ignore_errors=True)
			os.makedirs(dataDir)
		else:
			pass
	else:
		os.makedirs(dataDir)


def compressLocal(directory):
	''' function to compress the downloaded logs '''

	with tarfile.open(directory+'/compressedData.tar.gz', "w:gz") as compress:
		for root, dirs, files in os.walk(directory):
			for contents in dirs:
				compress.add(os.path.join(root, contents))


def copyLog(location, server):
	''' function to copy log '''

	if os.path.exists(downloadDir):
		downloadpath = os.path.join(downloadDir,server)
		os.makedirs(downloadpath, exist_ok=True)
		scpcommand = 'scp '+parse_arguments.user+'@'+server+':'+location+' '+downloadpath
		print('COPYING : {}'.format(location))
		subprocess.call(scpcommand, shell=True)
	else:
		print('ERROR: FileNotFound: {} not found'.format(downloadpath))
		sys.exit()


def compressLog(location, server):
	''' function to compress logs '''

	tarlog = os.path.join(location+'-'+server+'.tar.gz')
	ssh_to = datacenter.connect_to(server, username = parse_arguments.user, key = key)

	print('COMPRESSING : {}'.format(location))
	if parse_arguments.user == 'core':
		tarcommand = 'sudo tar -czf '+tarlog+' '+location
		clean = 'sudo rm '+tarlog
	else:
		tarcommand = 'tar -czf '+tarlog+' '+location
		clean = 'rm '+tarlog
	
	ssh_to.run_command(tarcommand)
	copyLog(tarlog, server)
	ssh_to.run_command(clean)


def downloadlogs():
	''' main function definition '''

	servers = parse_arguments.server[0].split(',')
	logpath = connectionCheck(servers)
	checkDir(downloadDir)

	for server in servers:
		print('\n----------SERVER : {}'.format(server))
		for log in logpath:
			if log[-2:] == 'gz':
				copyLog(log, server)
			else:
				compressLog(log, server)

	compressLocal(downloadDir)


if __name__ == "__main__":	

	try:

		parse = argparse.ArgumentParser()
		parse.add_argument('-f','--file', nargs='+', help='give a specific log to download', metavar='')
		parse.add_argument('-s','--server', nargs='+', help='server name to download logs', metavar='')
		parse.add_argument('-u','--user', help='user with access', metavar='')
		parse.add_argument('-p','--path', help='log file path', metavar='')
		parse_arguments = parse.parse_args()

		if parse_arguments.user == 'core':
			key = 'xxxx'
			downloadlogs()
		else:
			key = 'xxxx'
			downloadlogs()

		print('\n-------------RESULT-------------\n')
		print('Downloaded logs can be found in: {}\n'.format(downloadDir))

	except KeyboardInterrupt:
		pass
	except:
		print('ERROR: RunTimeError: Terminating program')