
import paramiko
import re

USERNAME = 'xxx'
KEY = 'xxx'

class connect_to:
	def __init__(self, server_name):
		self.ssh = paramiko.SSHClient()
		self.ssh.load_system_host_keys()
		self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		self.ssh.connect(hostname=server_name, username=USERNAME, key_filename=KEY)

	def run_command(self, command):
		if(self.ssh):
			stdin, stdout, stderr = self.ssh.exec_command(command)
			return stdout.read()
		else:
			print('Connection is not opened')

def extract_ipaddress(server,data):
    ''' function to extract ipaddress '''

    pattern = re.compile(r'addr:(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    ipaddress = re.search(pattern,data)
    print('SERVER {}: IPADDRESS {}'.format(server,ipaddress.group(1)))

def findipaddress(servers):
    ''' main function to find ipaddress '''

    for server in servers:
        ssh_to = connect_to(server)
        ipaddressdata = ssh_to.run_command('ifconfig').decode('utf-8')
        
        extract_ipaddress(server,ipaddressdata)

if __name__ == '__main__':

    try:
        servers = ['as1.xxx.com',
        'as2.xxx.com',
        'as3.xxx.com',
        'as4.xxx.com']

        findipaddress(servers)
    except KeyboardInterrupt:
        pass


# END