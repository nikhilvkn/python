import subprocess
import paramiko
import sys
import os

class connect_to:
    def __init__(self, server_name):
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=server_name, username=username, key_filename=key)
        self.sftpclient = self.ssh.open_sftp()

    def run_command(self, command):
        if(self.ssh):
            stdin, stdout, stderr = self.ssh.exec_command(command)
            return stdout.read()
        else:
            print('Connection is not opened')

key = 'xxx'
username = 'xxx'

if __name__ == '__main__':

    try:

        p = subprocess.Popen('sh query-servers.sh production db', 
                        shell=True, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT)
        print('Slave server in US Production:')
        print('------------------------------')
        for server in [x.decode('utf-8').strip('\n') for x in p.stdout.readlines()]:
            ssh_to = connect_to(server)
            db_command = "whatami | grep 'slave'"
            nw_command = "ifconfig | grep 'bond'"
            if not ssh_to.run_command(nw_command):
                if ssh_to.run_command(db_command):
                    print(server)

    except KeyboardInterrupt:
        pass