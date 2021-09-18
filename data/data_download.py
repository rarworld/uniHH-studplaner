#! /usr/bin/env python3

import requests
import json
import re
from bs4 import BeautifulSoup

BASE_URL="https://stine.uni-hamburg.de"
START_URL="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=ACTION&ARGUMENTS=-AgEMUVY1nAUlSVznOZcw~JqDZVA~w9CWPwKNqyhaITJcgSqnzyGbJmTprtCGaiIUdUVVihR-UkYJDPQXKi0T-6gT8bQeIBWwooNIVr4XL-l6vs0lyH6pMphEmULXU26qoHgDm6OcyvRleX-s476~uiiL-R~ZrEtnzqrSBYeXOfQbCcDNQ-Wcd-Pf2RaD5330-IJoY-aWYaApZZa8_"
#START_URL="/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSEDETAILS&ARGUMENTS=-N000000000000001,-N000650,-N0,-N379633497220262,-N379633497286263,-N0,-N0,-N0"
OVERVIEW_HREF_CLASS="auditRegNodeLink"
CATEGORY_HREF_CLASS="eventTitle"
TIME_PARSE_REGEX = re.compile('(\w\w),.*\[(\d\d:\d\d)\]-.*\[(\d\d:\d\d)\]')

def parseUebungsZeiten(vorlesung, soup):
    liList = soup.find_all('li', class_="tbdata listelement")
    vList=[]
    for li in liList:
        pList = li.find_all('p')
        
        tmp = {
            'name': pList[0].text,
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
    type = soup.find('input', {'name':'coursetyp'})['value']
    mainDataVorlesung = {
        'dozent': soup.find('span', id='dozenten').text,
        'name': soup.find('input', {'name':'shortdescription'})['value'],
        'type': soup.find('input', {'name':'coursetyp'})['value'],
        'id': soup.find('form', {'name':'courseform'}).h1.text.split('\n')[1].strip()
    }

    vorlesung = parseVorlesungsZeiten(mainDataVorlesung, soup)
    if type == "000000000000021":
       jsonObj['vorlesung'] = parseUebungsZeiten(mainDataVorlesung, soup) 
    else:
        jsonObj['vorlesung'] = [ parseVorlesungsZeiten(mainDataVorlesung, soup) ]

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
    
    if(len(link_liste) == 0):
        parseVorlesung(jsonObj, soup)


if __name__ == '__main__':
    overviewJson = { 
            'name': "Physik Overview",
            #'url': "https://stine.uni-hamburg.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSEDETAILS&ARGUMENTS=-N000000000000001,-N000605,-N0,-N377704122472643,-N377704122476644,-N0,-N0,-N3,-AQjAZPqHYPjAl3opkOoKAVIWXQSR3CYUCfDRNcjW6YYDNmd60vWL5HzwCOjBF4qAPHom9cgHIvURp7UH0YBmHe-5WxUawYqZWPMRHQd6qegpN7dRzRD5JmBBwegmkmBVZcUPL7f9tODwxHUH-OzHJQuUCfBwsYMpJOIR97dwMmSRIQMAyxoLomD7jOzHZxz5VRdLpVuoYeQRHVNoaHupQ4oPS3fBwQDZlVZHSW-mxxzWE4qKoPDRfYootQY5YVS59WQWFmIWjPIP5WDULcZHKxUPz4BRkvUWqxUKhVj56PzoeHYw3RqGAOzHoWSKCxuUZWqZmrMo5RjLKed5wQNUqPYHlco7Zmzm64SLfHSR3RNaARQctcUps7WUAxdPvHjmJQMRU7qGAHkZBOo5wPNLZVQUS7WPqRNofWfBZvUWLxoH9CfW9VBU5cBAtmURz4WLexuP34om97Dwb7YKPeZpwWqUVeZLxmUPDvY2ZOdoCmMKNQfWSv-mJfZLfQQUQegcNxN6FRWp-WoHQmfKIeMH8cgP6czLoRDRX3uR5cZitWgmWrq65YDR-CfLm7gP8WIRzOqGyfumCrUmTWqew4uWEvULLRdAKxMm53oLffUUDcomBcSRYYYHFOWeNfjKo3SKuevNdHbZIVgUAeWHwOfZk4B7AQzAHH-WMRB6le-ptWdKJfdH0vdGseMLDYYHmVjW5xYB9RNPlH-m67U5tcDKMOoHpxIRUPDWtv-RLxfywfQpM4Mm6voPPvB6P4YK07NR8",
            'url': START_URL,
            'links': []
        }
    
    parseOverview(overviewJson)

    with open('linkList.json', 'w') as outfile:
        json.dump( overviewJson, outfile, indent=2)