import sys
import requests
import json
import argparse
import os
import paramiko
import shutil
import tarfile
from collections import Counter
from socket import gaierror

paramiko.util.log_to_file('/tmp/paramiko.log')

example_text = '''
Example:
'''+str(sys.argv[0])+ ''' --user tivo --count 3
'''+str(sys.argv[0])+ ''' --user tivo --log <log name>
'''+str(sys.argv[0])+ ''' --user core --count 3
'''+str(sys.argv[0])+ ''' --user core --log <log name>
'''
parse = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
parse.add_argument("--count", help="count from latest to older")
parse.add_argument("--log", help="give a specific log to download")
#parse.add_argument("--multilog", help="give multiple logs to download")
parse.add_argument("--user", help="give the username with access", required=True)
parse_arguments = parse.parse_args()

key = 'xxxx'

homeDir = os.getenv("HOME")
scpDir = 'LogDirectory'
downloadDir = os.path.join(homeDir,scpDir)

match = {}
log, servers, fresh  = ([], [], [])

class connect_to:
	def __init__(self, server_name):
		self.ssh = paramiko.SSHClient()
		self.ssh.load_system_host_keys()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(hostname=server_name, username=parse_arguments.user, key_filename=key)
		self.sftpclient = self.ssh.open_sftp()

	def run_command(self, command):
		if(self.ssh):
			stdin, stdout, stderr = self.ssh.exec_command(command)
			return stdout.read()
		else:
			print('Connection is not opened')

	def exists(self, path):
		try:
			self.sftpclient.stat(path)
		except FileNotFoundError:
			return False
		else:
			return True

def appendPath(sourceList, location):
	merge = []
	for contents in sourceList:
		merge.append(location+'/'+contents)
	return merge

'''
def checkPath(location):
	# Format log location to use further in program
	if ssh_to.exists(location) == True:
		if location[-1] == '/':
			path = location[:-1]
			return path
		else:
			return location
	else:
		print('\nPath {} does not exist. Exiting...!!!\n'.format(location))
		terminate()
'''

def compressLog(availableData, server, location):
	# Compressing the remote files
	compressedFiles = {}
	serverName = server.split('.')[0]
	for contents in availableData.keys():
		for elements in availableData[contents]:
			#print('COMPRESSING : '+elements)
			print('COMPRESSING : {}'.format(elements))
			if parse_arguments.user == 'core':
				tar_command = 'sudo tar -czf '+elements+'-'+serverName+'.tar.gz '+elements
			else:
				tar_command = 'tar -czf '+elements+'-'+serverName+'.tar.gz '+elements
			ssh_to.run_command(tar_command)

			# Populate the compressesd values
			find_command = 'ls '+location+' | grep '+serverName
			tarValue = ssh_to.run_command(find_command).decode('utf8').strip('\n').split('\n')
			tarFinal = appendPath(tarValue, location)
			compressedFiles[server] = tarFinal
	return compressedFiles

def dictPrint(dictData):
	# To print the dictionary values for doing
	# troubleshooting
	for elements in dictData.keys():
		print('\n-------------'+elements+'-------------\n')
		for contents in dictData[elements]:
			print(contents)

def unique(list1): 
	# Below code helps to gather the unique elements
	# in the passed list
    unique_list = [] 
    for x in list1: 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list


def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
    wrapper.has_run = False
    return wrapper

@run_once
def checkDir(dataDir):
	if os.path.exists(dataDir) and os.path.isdir(dataDir):
		if os.listdir(dataDir):
			shutil.rmtree(dataDir, ignore_errors=True)
			os.makedirs(dataDir)
		else:
			pass
	else:
		os.makedirs(dataDir)

def copyFiles(scpData, server):
	# scp files from remote to local defining variables to prepair for SCP
	serverName = server.split('.')[0]
	downloadPath = os.path.join(downloadDir,serverName)
	if os.path.exists(downloadDir):
		downloadPath = os.path.join(downloadDir,serverName)
		os.makedirs(downloadPath, exist_ok=True)
		for elements in scpData.keys():
			for contents in scpData[elements]:
				scp_command = 'scp '+parse_arguments.user+'@'+server+':'+contents+' '+downloadPath
				print('COPYING : {}'.format(contents))
				os.system(scp_command)
	else:
		print('\nDirectory {} is not found, Exiting..!!\n'.format(downloadDir))


def compressLocal(directory):
	# To compress the donwloaded log in the directory
	with tarfile.open(directory+'/compressedData.tar.gz', "w:gz") as compress:
		for root, dirs, files in os.walk(directory):
			for contents in dirs:
				compress.add(os.path.join(root, contents))

def cleanUp(cleanData):
	# clean up tar file created in the server
	for elements in cleanData.keys():
		for contents in cleanData[elements]:
			if parse_arguments.user == 'core':
				clean_cmd = 'sudo rm '+contents
			else:
				clean_cmd = 'rm '+contents
			ssh_to.run_command(clean_cmd)

def terminate():
	# Terminate execution of the program
	sys.exit()

def checkName(good_words, given):
	# Below codd predicts the name of the log that
	# is entered manually
	answer = 0
	for elements in good_words: 
	    if given in elements:
	        return elements
	        answer += 1

	if answer == 0:
	    for elements in good_words:
	        count = 0
	        if count <= len(given):
	            for contents in given:
	                if contents in elements:
	                    match[contents] = elements
	                    count += 1
	                else:
	                    count += 1
	        else:
	            break
	    for elements in match.values():
	        log.append(elements)
	    count = Counter(log)
	    result = max(count, key=count.get)
	    
	    return result


if parse_arguments.log and parse_arguments.user:
	try:
		servers = input("\nEnter the list of servers [comma seperated]:\n").split(',')
		path = input("\nGive absolute path for file [not the file name]:\n")
		#path = checkPath(inputPath)
		logPath = path+'/'+parse_arguments.log
		checkDir(downloadDir)
		for server in servers:
			ssh_to = connect_to(server)
			if logPath[-2:] == 'gz':
				zippedFile = {}
				zippedFile[server] = logPath.split('\n')
				copyFiles(zippedFile, server)
			else:
				compressedFile = {}
				availableFile = {}
				availableFile[server] = logPath.split('\n')
				compressedFile = compressLog(availableFile, server, path)
				copyFiles(compressedFile, server)
				cleanUp(compressedFile)

		compressLocal(downloadDir)

	except KeyboardInterrupt:
		print('\nExiting the main program....!!\n')
		terminate()
	except gaierror:
		print('\nServer name is not given correclty, Exiting....!!\n')
		terminate()
	except paramiko.ssh_exception.AuthenticationException:
		print('\nHostname not found, Please recheckExiting..!!\n')
		terminate()
	else:
		print('\n-------------RESULT-------------\n')
		print('Downloaded logs can be found in: {}\n'.format(downloadDir))
		terminate()

# Main Program
if __name__ == "__main__":
	try:
		servers = input("\nEnter the list of servers [comma seperated]:\n").split(',')
		inputPath = input("\nGive absolute path for file [not the file name]:\n")

		# This finds the unique log names in the given location
		ssh_to = connect_to(servers[0])
		path = checkPath(inputPath)
		logData = ssh_to.run_command('ls '+path).decode('utf8').strip('\n').split('\n')

		print('Printing logData...............\n')
		print(logData)



		for values in logData[:-1]:
		    if '-' in values:
		        fresh.append(values.split('-')[0])
		    else:
		        fresh.append(values.split('.')[0])
		logData = unique(fresh)

		inputName = input("\nGive log file name [comma seperated]:\n")
		print('\n--------------------------------\n')
		if inputName not in logData:
			predictName = checkName(logData,inputName)
			predict = input('Do you mean {}? [Y/N]: '.format(predictName))
			if predict == 'y' or predict == 'Y':
				logName = predictName
			else:
				print('\n::Following logs are found in server: \n')
				for values in logData:
					print(values)
				logName = input('\nPlease specify [comma seperated]:\n')
		else:
			logName = inputName

		# if provided file contains '.log' or '.log.gz', we need to trim
		# the file name to get just the name
		count_cmd = 'ls '+path+' | grep '+logName+' | tail -n '+parse_arguments.count
		
		# Getting absolute file names from servers
		for server in servers:
			print('\n-------------'+server+'-------------\n')
			zipped, available = ([], [])
			zippedFile = {}
			availableFile = {}
			ssh_to = connect_to(server)
			logFile = ssh_to.run_command(count_cmd).decode('utf8').strip('\n').split('\n')

			# Decorating the final_list to obtain the file path
			for elements in logFile:
				if elements[-2:] == 'gz':
					zipped.append(path+'/'+elements)
				else:
					available.append(path+'/'+elements)

			# Check the status of downloadDir
			checkDir(downloadDir)

			# Cross check the corresponding list and call function	
			if zipped:
				zippedFile = {}
				zippedFile[server] = zipped
				copyFiles(zippedFile, server)
			else:
				pass

			if available:
				compressedFile = {}
				availableFile = {}
				availableFile[server] = available
				compressedFile = compressLog(availableFile, server, path)
				copyFiles(compressedFile, server)
			else:
				pass

			# Claeaning up the tar files
			cleanUp(compressedFile)	
		
		# Compressing downloaded logs
		compressLocal(downloadDir)

	except KeyboardInterrupt:
		print('\nExiting the main program..!!\n')
		terminate()
	except gaierror:
		print('\nServer name is not given correclty, Exiting..!!\n')
		terminate()
	except paramiko.ssh_exception.AuthenticationException:
		print('\nHostname not found, Please recheckExiting..!!\n')
		terminate()
	else:
		print('\n-------------RESULT-------------\n')
		print('Downloaded logs can be found in: {}\n'.format(downloadDir))
		terminate()


