# Downloading Logs

I would say, my developing team needs logs for troubleshooting when we are hit with an incident. In micro service architecture,
we know the needs for service logs. How I can achieve this, keeping in mind of these points,
- There is on premise and cloud datacenter
- Micro services can be deployed in multiple environments
- The path can be differnet for each service logs
- Logs name will be same in all instances of micro service
- How to zip these all

How can I tackle these things :thinking:, honeslty I can say there were many more points which I sorted out while creating this
program, above given as few amoung them. Just sharing my idea on this. May be this gives a good starting point for all.

Created this program which does every thing as discussed above, even I added a logic where, if you specify a directory path to 
fetch the log, and give a wrong log file name, my logic will give you a suggestion saying "Are you looking for xyz log name?"
Isn't that cool :man_dancing:





```
Maintainer: Nikhil Narayanan [nikhilvkn@yahoo.com]
```
