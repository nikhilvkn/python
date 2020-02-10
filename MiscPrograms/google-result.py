#This program will find top 7 google search results in your default browser

import webbrowser
import requests
import sys
import bs4

print('Finding top 7 results for you....')
res = requests.get('http://google.com/search?q=' + ' '.join(sys.argv[1:]))
try:
    res.raise_for_status()
except Exception as e:
     print('There was a problem: %s' % (e))
# Retrieve top search result links.
soup = bs4.BeautifulSoup(res.text, "html.parser")
# Open a browser for result.
linkElems = soup.select('.r a')
numOpen = min(7, len(linkElems))
for i in range(numOpen):
    webbrowser.open('http://google.com' + linkElems[i].get('href'))
