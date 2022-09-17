#! /usr/bin/env python3

from datetime import datetime,time
import json

class NaviCreator:

    def __init__(self, main_config) -> None:
        self.config = main_config['navi']
        self.debug = self.config['debug']
        self.studiengange = main_config['studiengange']
    

    def navi(self):
        result_json = []

        for gang in self.studiengange:
            working_json = self.__open_link_list(self.config['input_prefix']+gang['short']+".json")
            result_json.append(self.__clean_data(working_json))
            
        with open(self.config['file_name'], 'w') as outfile:
            json.dump( result_json, outfile, indent=2)


    def __open_link_list(self, filename):
        with open(filename) as json_file:
            json_object = json.load(json_file)
            json_file.close()
        return json_object


    def __clean_data(self, working_json):
        return_json = {
            'name': working_json['name'],
            'submenu': [],
            'entries': []
        }
        # print(linksList['name'])
        if(len(working_json['links'])==0):
            if 'vorlesung' in working_json:
                menu_entry=[]
                for tmp in working_json['vorlesung']:
                    menu_entry.append({
                        'id': tmp['id'],
                        'name': tmp['name']
                    })
                return_json['entries'] = menu_entry
        else:
            for link in working_json['links']:
                return_json['submenu'].append(self.__clean_data(link))
        return return_json


if __name__ == "__main__":
    with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    navi_creator = NaviCreator(jsonObject)
    navi_creator.navi()