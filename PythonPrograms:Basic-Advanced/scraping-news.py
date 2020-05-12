from bs4 import BeautifulSoup
import requests
import pprint


def main(links,votes):
    data = []
    for idx, item in enumerate(links):
        text = item.getText()
        url = item.get('href', None)
        points = votes[idx].select('.score')
        if len(points):
            vote = int(points[0].getText().replace(' points',''))
            if vote > 99:
                data.append({'Title': text, "Url": url, "Votes": vote})
                data = sorted(data, key=lambda x: x['Votes'], reverse=True )
    pprint.pprint(data)    


if __name__ == '__main__':
    resonse = requests.get('https://news.ycombinator.com/')
    soup = BeautifulSoup(resonse.text, 'html.parser')
    
    links = soup.select('.storylink')
    votes = soup.select('.subtext')
    main(links,votes)