#! /usr/bin/env python3

import requests
import json
from bs4 import BeautifulSoup

BASE_URL="https://stine.uni-hamburg.de"
START_URL="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AgEMUVY1nAUlSVznOZcw~JqDZVA~w9CWPwKNqyhaITJcgSqnzyGbJmTprtCGaiIUdUVVihR-UkYJDPQXKi0T-6gT8bQeIBWwooNIVr4XL-l6vs0lyH6pMphEmULXU26qoHgDm6OcyvRleX-s476~uiiL-R~ZrEtnzqrSBYeXOfQbCcDNQ-Wcd-Pf2RaD5330-IJoY-aWYaApZZa8_"
#START_URL="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSEDETAILS&ARGUMENTS=-N000000000000001,-N000650,-N0,-N379633497220262,-N379633497286263,-N0,-N0,-N0"
OVERVIEW_HREF_CLASS="auditRegNodeLink"
CATEGORY_HREF_CLASS="eventTitle"


def parseVorlesung(jsonObj, soup):
    jsonObj['vorlesung'] = {
        'dozent': soup.find('span', id='dozenten').text,
        'name': soup.find('input', {'name':'shortdescription'})['value'],
        'type': soup.find('input', {'name':'coursetyp'})['value'],
        'id': soup.find('form', {'name':'courseform'}).h1.text.split('\r\n')[1]
    }
    table = soup.find('table', class_="tb list rw-table rw-all")
    tbody = table.find_all('tr')
    zeiten=[]
    for tr in tbody:
        if(tr.get('class')==None):
            tds = tr.find_all('td')
            if(len(tds) > 1):
                zeit={
                    'day': tds[1].text.split(',')[0],
                    'start': tds[2].text,
                    'end': tds[3].text,
                    'hs': tds[4].text.strip()
                }
                #zeit=f"{tds[1].text.split(',')[0]} {tds[2].text}-{tds[3].text} in {tds[4].text.strip()}"
                if(not zeit in zeiten):
                    zeiten.append(zeit)
    jsonObj['vorlesung']['time']= zeiten

def parseOverview(jsonObj):
    print(f"Parsing {jsonObj['name']}")
    start_url = jsonObj['url']
    html_text = requests.get(BASE_URL + start_url, headers={'Accept-Encoding':'utf-8'}).content.decode('utf-8', 'ignore')
    soup = BeautifulSoup(html_text, 'html.parser')

    link_liste=jsonObj['links']

    for link in soup.find_all('a', class_=[OVERVIEW_HREF_CLASS,CATEGORY_HREF_CLASS]):
        link_liste.append({ 
            'name': link.text,
            'url': link.get('href'),
            'links': []
        })    

    for l in link_liste:
        parseOverview(l)
    
    if(len(link_liste) == 0):
        parseVorlesung(jsonObj, soup)


if __name__ == '__main__':
    overviewJson = { 
            'name': "Physik Overview",
            'url': START_URL,
            'links': []
        }
    
    parseOverview(overviewJson)

    with open('linkList.json', 'w') as outfile:
        json.dump( overviewJson, outfile, indent=2)