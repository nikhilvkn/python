import pyperclip
import shelve
import sys 

pwdList = shelve.open('UserPwd')
if len(sys.argv) == 2 and sys.argv[1].lower() == '--help':
	print('Usage: ./passwordSafer.py [-l | -a | -d | -m]')
	print('-l : to list the entire accounts in database\n-a : to add a new account to database\n-d : to delete an existing account\n-g : helps to get the password of an account in your clipboard [ ./passwordSafe.pl -g <account_name> ]\n-m : modify the value of an existing account')
	sys.exit()

#Function to Add account details..!!!
def addMe():
	while True:
		print('Enter the name of account you wish to add : [Or nothing to exit]')
		account = input().split(",")
		if account == '':
			sys.exit()
		if account not in pwdList:
			print('Enter the password :')
			pwd = input()
			pwdList[account] = pwd
			print('Successfully Updated Database!!')
			anAccount = input('Do you want to add another account (y/n): ')
			if anAccount == 'y':
				continue
			else:
				sys.exit()
		else:
			print('Account ' + account + ' exists in Database. To view the details, use (-l | -g) option')

#Function to Delete the account...!!!
def deleteMe():
	while True:
		print('Enter the account name to delete : [Or nothing to exit]')
		delAccount = input()
		if delAccount == '':
			sys.exit()
		if delAccount not in pwdList:
			print('Account not found in database')
			continue
		else:
			del pwdList[delAccount]
			print('Successfully Deleted Account!!')

#Function to List all accounts...!!!
def listMe():
	print('The complete list of Accounts are :')
	for k in pwdList.keys():
		print('\t ' + k)

#Function to Get the value in Clipboard...!!!
def getMe():
	if sys.argv[2] in pwdList:
		pyperclip.copy(pwdList[sys.argv[2]])
		print('Password copied to Clipboard')
	else:
		print('Account not in Database, Check with ( -l ) option ')

#Function to Modify account value...!!!
def modifyMe():
	print('You can give your account name here : [Or nothing to exit]')
	accName = input()
	if accName == '':
		sys.exit()
	if accName in pwdList:
		print('Account is present in Database, Please add the new value')
		newValue = input()
		pwdList[accName] = newValue
		print('Account Successfully Modified')
	else:
		print('Account ' + accName + ' not found in Database')
		toList = input('Do you want to list all Account (y/n): ')
		if toList == 'y':
			listMe()
		else:
			sys.exit()

#Main Program
if len(sys.argv) == 2 and sys.argv[1].lower() == '-a':
	addMe()
elif len(sys.argv) == 2 and sys.argv[1].lower() == '-d':
	deleteMe()
elif len(sys.argv) == 2 and sys.argv[1].lower() == '-l':
	listMe()	
elif len(sys.argv) == 2 and sys.argv[1].lower() == '-m':
	modifyMe()
elif len(sys.argv) == 3 and sys.argv[1].lower() == '-g':
        getMe()
else:
        print('Check the syntax with --help')	

#Close the Shelve variable
pwdList.close()	

