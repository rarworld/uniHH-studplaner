#! /usr/bin/env python3

import datetime
import json
from bs4 import BeautifulSoup
import requests
import re

class Parser:

    def __init__(self, main_config) -> None:
        self.config = main_config['parser']
        self.debug = self.config['debug']
        self.studiengange = main_config['studiengange']
        self.parsing_date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.OVERVIEW_HREF_CLASS= self.config['OVERVIEW_HREF_CLASS']
        self.CATEGORY_HREF_CLASS= self.config['CATEGORY_HREF_CLASS']
        self.TIME_PARSE_REGEX = re.compile('(\w\w),.*\[(\d\d:\d\d)\]-.*\[(\d\d:\d\d)\]')
    

    def parsing(self):
        for gang in self.studiengange:
            print(f"parsing {gang['name']}")
            overview_json = self.parse_studiengang(gang)
            with open(overview_json['file'], 'w') as outfile:
                json.dump( overview_json, outfile, indent=2)


    def parse_studiengang(self, studiengang) -> json:
        data_json = {
            'file': self.config['file_name_prefix'] + studiengang['short'] + ".json",
            'name': studiengang['name'],
            'url': studiengang['url'],
            'date': self.parsing_date,
            'links': []
        }
        self.__parse_overview(data_json)
        return data_json


    def __download(self, url):
        html_text = requests.get(url, headers={'Accept-Encoding':'utf-8'}).content.decode('utf-8', 'ignore')
        return BeautifulSoup(html_text, 'html.parser')


    def __parse_overview(self, data_json):
        url = self.config['baseUrl'] + data_json['url']
        soup = self.__download(url)
        link_liste=data_json['links']

        for link in soup.find_all('a', class_=[self.OVERVIEW_HREF_CLASS, self.CATEGORY_HREF_CLASS]):
            link_liste.append({ 
                'name': link.text,
                'url': link.get('href'),
                'links': []
            })    

        for ll in link_liste:
            self.__parse_overview(ll)
        
        if(soup != None and len(link_liste) == 0):
            self.__parse_vorlesung(soup, data_json)


    def __parse_vorlesung(self, soup, data_json):
        entry = soup.find('input', {'name':'coursetyp'})
        if entry != None:
            entry_type = entry['value']
            main_data_vorlesung = {
                'dozent': soup.find('span', id='dozenten').text,
                'name': soup.find('form', {'name':'courseform'}).h1.text.split('\n')[2].strip(),
                'short': soup.find('input', {'name':'shortdescription'})['value'],
                'type': entry_type,
                'id': soup.find('form', {'name':'courseform'}).h1.text.split('\n')[1].strip()
            }

            data_json['vorlesung'] = [ self.__parse_vorlesungs_zeiten(main_data_vorlesung, soup) ]
            data_json['vorlesung'] += self.__parse_uebungs_zeiten(main_data_vorlesung, soup)             
        else:
            print(f" - Empty Liste")


    def __parse_uebungs_zeiten(self, vorlesung, soup):
        li_list = soup.find_all('li', class_="tbdata listelement")
        vorlesung_list=[]
        for li in li_list:
            p_list = li.find_all('p')
            
            tmp = {
                'name': vorlesung['name'],
                'groupname': p_list[0].text,
                'dozent': p_list[1].text,
                'type': vorlesung['type'],
                'id': f"{vorlesung['id']}_{len(vorlesung_list)}"
            }

            m = self.TIME_PARSE_REGEX.match(p_list[2].text)
            if m is not None:
                tmp['time']= [{           
                    'day': m.group(1),
                    'start': m.group(2),
                    'end': m.group(3),
                    'hs': "",
                }]
            vorlesung_list.append(tmp)
        return vorlesung_list


    def __parse_vorlesungs_zeiten(self, vorlesung, soup):
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
                    if( zeit not in zeiten):
                        zeiten.append(zeit)
                else:
                    vorlesung['blub'] = tds[0].text
                    if(self.debug):
                        print(f" - {tds[0].text}")
        vorlesung['time'] = zeiten
        return vorlesung


if __name__ == "__main__":
    with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    parser = Parser(jsonObject)
    parser.parsing()