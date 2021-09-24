#! /usr/bin/env python3

import requests
import json
import re
from bs4 import BeautifulSoup

BASE_URL="https://stine.uni-hamburg.de"
START_URL_PHY="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AgEMUVY1nAUlSVznOZcw~JqDZVA~w9CWPwKNqyhaITJcgSqnzyGbJmTprtCGaiIUdUVVihR-UkYJDPQXKi0T-6gT8bQeIBWwooNIVr4XL-l6vs0lyH6pMphEmULXU26qoHgDm6OcyvRleX-s476~uiiL-R~ZrEtnzqrSBYeXOfQbCcDNQ-Wcd-Pf2RaD5330-IJoY-aWYaApZZa8_"
START_URL_INF="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-A4q44qENDI4Y8Q6xak1Qw~rJ2ofruoap-IgfTiZdgy0d977RZdXkQzskSbPkfl-RrZTJvU3o2JIMambmYchAELDJ3mz9T2KtyxBiTtNz8YJfAY0HMf2GD2StN83Xr0hi8Ex~R35msxz-QyHIzMOeayDvoIiU3f73-jQ0o6nJMJdlfEyWfk7lmpy8mzHfH1orUFlmvoNsWdUCwpK4_"
OVERVIEW_HREF_CLASS="auditRegNodeLink"
CATEGORY_HREF_CLASS="eventTitle"
TIME_PARSE_REGEX = re.compile('(\w\w),.*\[(\d\d:\d\d)\]-.*\[(\d\d:\d\d)\]')

def parseUebungsZeiten(vorlesung, soup):
    liList = soup.find_all('li', class_="tbdata listelement")
    vList=[]
    for li in liList:
        pList = li.find_all('p')
        
        tmp = {
            'name': vorlesung['name'],
            'groupname': pList[0].text,
            'dozent': pList[1].text,
            'type': vorlesung['type'],
            'id': f"{vorlesung['id']}_{len(vList)}"
        }

        m = TIME_PARSE_REGEX.match(pList[2].text)
        if not m is None:
            tmp['time']= [{           
                'day': m.group(1),
                'start': m.group(2),
                'end': m.group(3),
                'hs': "",
            }]
        vList.append(tmp)
    return vList


def parseVorlesungsZeiten(vorlesung, soup):
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
    vorlesung['time'] = zeiten
    return vorlesung


def parseVorlesung(jsonObj, soup):
    test = soup.find('input', {'name':'coursetyp'})
    if test != None:
        type = test['value']
        mainDataVorlesung = {
            'dozent': soup.find('span', id='dozenten').text,
            'name': soup.find('form', {'name':'courseform'}).h1.text.split('\n')[2].strip(),
            'short': soup.find('input', {'name':'shortdescription'})['value'],
            'type': type,
            'id': soup.find('form', {'name':'courseform'}).h1.text.split('\n')[1].strip()
        }

        jsonObj['vorlesung'] = [ parseVorlesungsZeiten(mainDataVorlesung, soup) ]
        jsonObj['vorlesung'] += parseUebungsZeiten(mainDataVorlesung, soup)             
    else:
        print(f" - Empty Liste")


def parseOverview(jsonObj):
    print(f"Parsing {jsonObj['name']}")
    start_url = jsonObj['url']
    html_text = requests.get(BASE_URL + start_url, headers={'Accept-Encoding':'utf-8'}).content.decode('utf-8', 'ignore')
    #with open('testUbung.html', 'r') as file:
    #    html_text = file.read()
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
    
    if(soup != None and len(link_liste) == 0):
        parseVorlesung(jsonObj, soup)


overviewPhysik = { 
    'file':"linkList_Phy.json",
    'name': "Physik Overview",
    'url': START_URL_PHY,
    'links': []
}
overviewCis = { 
    'file':"linkList_Inf.json",
    'name': "Computing in Science - Physik Overview",
    'url': START_URL_INF,
    'links': []
}
overviewTest = { 
    'file':"linkList_tmp.json",
    'name': "Computing in Science - Physik Overview",
    'url': "/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSEDETAILS&ARGUMENTS=-N000000000000001,-N000650,-N0,-N379853809291016,-N379853809235017,-N0,-N0,-N0",
    'links': []
}

#overviewJson=overviewPhysik
#overviewJson=overviewCis
overviewJson=overviewTest

parseOverview(overviewJson)

with open(overviewJson['file'], 'w') as outfile:
    json.dump( overviewJson, outfile, indent=2)