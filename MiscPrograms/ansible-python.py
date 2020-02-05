import subprocess
import time

def runansible():
    cmd = ["ansible-playbook",
           "-i",
           "inventory",
           "playbook.yml",
           "-v"]
    process = subprocess.Popen(cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            )
    print('STATUS: installation in progress')
    while True:
      time.sleep(7)
      poll = process.poll()
      if poll is not None:
        print('STATUS: installation completed')
        break
        

runansible()
