from paramiko.auth_handler import AuthenticationException, SSHException
from func_timeout import FunctionTimedOut, func_set_timeout
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from scp import SCPClient, SCPException
from pathlib import Path
import subprocess
import requests
import time
import sys
import os
import re

servers = ['xxx']
USERNAME = 'xxx'
KEY = 'xxx'
partition = '/'
artifactoryurl = 'xxx'

@func_set_timeout(9)
class RemoteConnect:
    
    def __init__(self,host):
        self.host = host
        self.client = None
        self.scp = None
        self.__connect()
    
    def __connect(self):
        try:
            self.client = SSHClient()
            self.client.load_system_host_keys()
            self.client.set_missing_host_key_policy(AutoAddPolicy())
            self.client.connect(hostname=self.host, 
                                username=USERNAME, 
                                key_filename=KEY)
            self.scp = SCPClient(self.client.get_transport())
        except AuthenticationException as error:
            print('Authentication Failed: Please check your network/ssh key')
        finally:
            return self.client
        
    def disconnect(self,flag=False):
        self.client.close()
        if flag is True:
            self.scp.close()

    def exec_command(self,command):
        if self.client is None:
            self.client == self.__connect()
        stdin,stdout,stderr = self.client.exec_command(command)
        return stdout.read()
                
    def transfer(self,file,remotepath):
        try:
            if self.client is None:
                self.client = self.__connect()
            self.scp.put(file,
                         remotepath,
                         recursive=True)
        except SCPException as error:
            print('SCPException: Failed tansferring data')


def diskcheck():
    ''' function to check disk/ mount status & transfer '''
    
    pattern = re.compile(r"(\d+%)\s(/.*)")
    more_disk = []
    
    try:
        print('STEP: Checking Disk & Mount')
        for server in servers:
            ssh_to = RemoteConnect(server)
            diskdata = ssh_to.exec_command('df -h').decode('utf-8')
            data = pattern.findall(diskdata)
            percentage = [value[0][:-1] for value in data if partition in value][0]
            if int(percentage) >= 98:
                more_disk.append(server)
            ssh_to.disconnect()

        if more_disk:
            print('''
            High Disk Usage:
            {}
            Please check space and try again
            '''.format([value for value in more_disk]))
            sys.exit()
        else:
            pass
        
    except FunctionTimedOut:
        print('SERVER: {} timedout, please check mount status'.format(server))
        sys.exit()


def filestatus(name,directory,startwith=True):
    '''function to check presence of file'''
    
    name_store = []
    print('STEP: Finding correct RPM')
    if not startwith==False:
        [name_store.append(filename) for filename in os.listdir(directory) if filename.startswith(name)]
                
    if len(name_store) > 1:
        name_store.sort()
        return name_store[-1]
    return name_store[0]


def checkmd5(filepath):
    '''function to check/confirm md5 of an rpm'''

    pattern = re.compile(r'\s([a-zA-Z0-9]+)$')
    cmd = ["md5",
           filepath]
    process = subprocess.check_output(cmd).decode('utf-8').strip()
    md5value = pattern.findall(process)[0]

    response = requests.get("{}{}".format(artifactoryurl,md5value))
    if response.status_code is 200:
        pass
    else:
        print('ERROR: Checksum not matching..!!')
        sys.exit()


def transferdata(lfile,path):
    ''' function to transfer data to remote '''
    
    print('STEP: Transfer RPM')
    for server in servers:
        ssh_to = RemoteConnect(server)
        print('Transferring: {}'.format(server))
        ssh_to.transfer(lfile,path)
        ssh_to.disconnect()


def runansible():
    ''' function to run ansible code on remote '''
    
    cmd = ["ansible-playbook",
           "-i",
           "inventory",
           "playbook.yml",
           "-v"]
    process = subprocess.Popen(cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            )
    print('STATUS: Installation in progress')
    while True:
      time.sleep(7)
      poll = process.poll()
      if poll is not None:
        print('STATUS: Installation completed')
        break


if __name__ == '__main__':

    try:

        directory = os.path.join(os.path.expanduser('~'),'Downloads/')
        logo = filestatus('sd_en_name',directory)
        localfile = os.path.join(directory,logo)
        checkmd5(localfile)
        remotepath = '/tmp/'
        diskcheck()
        transferdata(localfile,remotepath)
        runansible()

    except KeyboardInterrupt:
        pass
    finally:
        print('Execution Completed..!!')