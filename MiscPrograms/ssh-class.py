from paramiko.auth_handler import AuthenticationException, SSHException
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from scp import SCPClient, SCPException

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