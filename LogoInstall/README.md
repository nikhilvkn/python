# Logo Install Program

Given a task to automate rpm install in a set of servers, which has following details,
1. User name for each server is same
2. Root password for each server is different
3. Source of rpm is artifactory. Downloaded rpm to local machine
4. If the rpm is already installed, need to skip that server
5. Need to transfer the rpm from local machine to remote server

All these points are considered in this program, along with logic that queries if the transfer is completed, also checks and
find the latest rpm from the list of rpm from the local machine.

Transfer will only happen, 
1. If there is adequate disk space in remote server
2. There is no mount issues in remote server

Above two points are also considered and checked before program start a rpm trasfer followed by install and clean up of rpm
in remote server



```
Maintainer: Nikhil Narayanan [nikhilvkn@yahoo.com]
```

