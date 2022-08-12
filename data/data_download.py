#! /usr/bin/env python3

import sys
import requests
import datetime
import json
import re
from bs4 import BeautifulSoup

BASE_URL="https://stine.uni-hamburg.de"
#WS 2021/2022
#START_URL_PHY="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AgEMUVY1nAUlSVznOZcw~JqDZVA~w9CWPwKNqyhaITJcgSqnzyGbJmTprtCGaiIUdUVVihR-UkYJDPQXKi0T-6gT8bQeIBWwooNIVr4XL-l6vs0lyH6pMphEmULXU26qoHgDm6OcyvRleX-s476~uiiL-R~ZrEtnzqrSBYeXOfQbCcDNQ-Wcd-Pf2RaD5330-IJoY-aWYaApZZa8_"
#START_URL_INF="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-A4q44qENDI4Y8Q6xak1Qw~rJ2ofruoap-IgfTiZdgy0d977RZdXkQzskSbPkfl-RrZTJvU3o2JIMambmYchAELDJ3mz9T2KtyxBiTtNz8YJfAY0HMf2GD2StN83Xr0hi8Ex~R35msxz-QyHIzMOeayDvoIiU3f73-jQ0o6nJMJdlfEyWfk7lmpy8mzHfH1orUFlmvoNsWdUCwpK4_"
#SS 2022
#START_URL_PHY="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AnIpuyxaapGZ6HBS~Sb8MMdpL-s~63sHFxOUTtzKGkWy-2CK-WNI1ReuUx582PRAYhf1Z4M3MILKyjgoDmp1jsAZEzKiiq9C4Uagewpa31eLauzyxg08aMKb8tTO9zFGLSx8NoNtW-ZzD-I4Wrr550asXzKIlsmDBgta0aTG2ovmuBIjPPtUxTyPq2WHXUFTa~Dwe7QFXjStOUKI_"
#START_URL_INF="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AkpPWSqBzz9k7prVUd4jTWC3TatsKNfGZybddd38-tGtrn6Ef5EdaTj2FE5QGZb5tUkV4rO~uezamrpA21mnXu9GJnRdg98DTQ0XezlqRE2romddYh6lxGN6mCa3ye64yacOAmxL5CwwFgFR2ksSGn4zqbgCZDrCj9b6gjnDW9QJ5Zvt~PpR-TS~k-Evx5XgDXYzjWJ5BVCVkU7k_"
#WS 2022/2023
START_URL_PHY="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AoepE19QJAGYj~5rV5xzEPC4kOX1EaUP8Wz~Di4l2Ad8a5Wszr72wW-hUgXhfLTvSHV1G97FCEct39iY3BvGmXDZ0lSUm8nFEL~qFNm~mKkZOYGU8HDlXq68PzRlDB7YZEC~hvJbLJebdpJa48X9okPvDpsz-CEtFaKvoveCHrRh7ACrOCgVJXmrFsTPjY8A6AE6Glmf8z6ox-No_"
START_URL_INF="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AsBlEbB-LJAPQO3rmLgIAUFC8xHSt6pwP2Uidt6PwScbv-F0FaOyWU4DLJuGcjEqqkP-U-fKYyDfWNlO0bxu9~yqXWYOSGXMP8Z~DBnLd-owy0rgTmYiSB3cBJju15VPR4UNMIN5938RjvJws~WdQpRf9o6X-DXnx4SJVncO2f7Z2J1igQ8urCCz5yVN7MINKOlnGYlBGlFRlNnI_"
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
            else:
                vorlesung['blub'] = tds[0].text
                print(f" - {tds[0].text}")
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
    'name': "Physik",
    'url': START_URL_PHY,
    'links': []
}
overviewCis = { 
    'file':"linkList_Inf.json",
    'name': "Computing in Science - Physik",
    'url': START_URL_INF,
    'links': []
}
overviewTest = { 
    'file':"linkList_Tmp.json",
    'name': "Computing in Science - Physik",
    'url': "/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSEDETAILS&ARGUMENTS=-N000000000000001,-N000650,-N0,-N379633498964364,-N379633498962365,-N0,-N0,-N0",
    'links': []
}

print( 'Number of arguments:', len(sys.argv), 'arguments.')
print( 'Argument List:', str(sys.argv))
print( sys.argv[0])

if(len(sys.argv) == 2):
    if(sys.argv[1] == 'cis'):
        overviewJson=overviewCis
    elif(sys.argv[1] == 'phy'):
        overviewJson=overviewPhysik
    elif(sys.argv[1] == 'test'):
        overviewJson=overviewTest
    else:
        exit()
else:
    exit()

parsingDate = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

parseOverview(overviewJson)

overviewJson['date'] = parsingDate
with open(overviewJson['file'], 'w') as outfile:
    json.dump( overviewJson, outfile, indent=2)