# This program will help open a set of URL's for a particular topic

import webbrowser 
import shelve
import sys

website = shelve.open('myWebsites.db',writeback=True)
if len(sys.argv) == 2 and sys.argv[1].lower() == '--help':
    print('\nUsage: ./urlDictionary.py [-l | -a | -d | -m | -b]')
    print('\n-l : to list all topics [./urlDictionary.py -l]\n\n-a : to add a new topic [./urlDictionary.py -a <topic name>]\n\n-d : to delete an existing topic [./urlDictionary.py -d <topic name>]\n\n-m : modify the value of an existing topic [./urlDictionary.py -m <topic name>]\n\n-b : browse contents in your default browser  [./urlDictionary.py -b <topic name>]\n')
    sys.exit()

def addMe():
    if sys.argv[2] not in website:
        webAddress = input('Give addresses seperated by comma: ').split(",")
        website[sys.argv[2]] = webAddress
        print('Added Successfully')
    else:
        print('Topic ' + str(sys.argv[2]) + ' already exists. To view the details use -l option')

def listMe():
    print('The complete list of Topics are :')
    keys = list(website.keys())
    keys.sort()
    for k in keys:
        print('\t' + k)

def browseMe():
    if sys.argv[2] in website:
        for url in website[sys.argv[2]]:
            webbrowser.open(url,new=1)
    else:
        print('Topic not found, check with ( -l ) option and continue')

def modifyMe():
    if sys.argv[2] in website:
        newAddress = input('Give address : ')
        website[sys.argv[2]].append(newAddress)
        print('Modified Successfully')
    else:
        print('Topic not found... add a Topic using -a option')

def deleteMe():
    if sys.argv[2] in website:
        del website[sys.argv[2]]
        print('Deleted ' + str(sys.argv[2]) + ' successfully')
    else:
        print('Topic ' + str(sys.argv[2]) + 'not found. Use -l to view the topic names')
if len(sys.argv) == 3 and sys.argv[1].lower() == '-a':
    addMe()  # Function call to add topic and address
elif len(sys.argv) == 2 and sys.argv[1].lower() == '-l':
    listMe() # Function call to list all the topic's in myWebsite.db
elif len(sys.argv) == 3 and sys.argv[1].lower() == '-b':
    browseMe() # Function call to browse the url's in your default browser
elif len(sys.argv) == 3 and sys.argv[1].lower() == '-m':
    modifyMe() # Function call to add address to a particular topic
elif len(sys.argv) == 3 and sys.argv[1].lower() == '-d':
    deleteMe() # Function call to delete a particular topic and associated addresses

website.close()
