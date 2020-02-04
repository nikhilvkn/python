
from func_timeout import FunctionTimedOut, func_set_timeout
import paramiko
import time
import sys

servers = ['xxxx']
USERNAME = 'xxxx'
KEY = 'xxx'

@func_set_timeout(4)
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


if __name__ == '__main__':
    
    partition = '/'
    more_disk = []
    pattern = re.compile(r"(\d+%)\s(/.*)")

    try: 
        for server in servers:
            ssh_to = connect_to(server)
            diskdata = ssh_to.run_command('df -h').decode('utf-8')
            data = pattern.findall(diskdata)
            percentage = [value[0][:-1] for value in data if partition in value][0]
            if int(percentage) >= 98:
                more_disk.append(server)         

        if more_disk:
            print('''
            High Disk Usage:
            {}
            Please check space and try again
            '''.format([value for value in more_disk]))
            sys.exit()
        else:
            print('Disk and Mount looks fine..!!')

    except FunctionTimedOut:
        print('SERVER: {} timedout, please check mount status'.format(server))
        sys.exit()
    except KeyboardInterrupt:
        pass

