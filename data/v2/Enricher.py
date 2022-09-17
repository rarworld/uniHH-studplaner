#! /usr/bin/env python3

import json
import datetime
import re

class Enricher:

    def __init__(self, main_config) -> None:
        self.config = main_config['enricher']
        self.debug = self.config['debug']
    

    def enrich(self) -> json:
        input_object = self.__load_data(self.config['input'])
        input_object['file_name'] = self.config['file_name']

        self.__enrich_ubung_id(input_object)

        with open(self.config['file_name'], 'w') as outfile:
            json.dump( input_object, outfile, indent=2)


    def __load_data(self, filename):
        with open(filename) as json_file:
            json_object = json.load(json_file)
            json_file.close()
        return json_object


    def __enrich_ubung_id(self, data_json):
        ubg_vl_dict = self.__add_ubg_to_vl(data_json['data'])
        self.__add_vl_to_ubg(data_json['data'], ubg_vl_dict)


    def __add_ubg_to_vl(self, all_lessons):
        lessons_count = len(all_lessons)
        ubg_vl_dict = {}

        for i in range(lessons_count-1):
            vl = all_lessons[i]
            if( 'short' in vl and vl['short'] != "" and vl['type'] == "000000000000022"):
                    ubg = all_lessons[i+1]
                    if(ubg['type'] == "000000000000021"):
                        vl_clean_name = vl['name'].replace("Vorlesung ","").lower()
                        if( vl_clean_name in ubg['name'].lower() ):
                            ubg_vl_dict[ubg['id']]=vl['id']
                            vl["base"] = ubg['id']
        return ubg_vl_dict


    def __add_vl_to_ubg(self, all_lessons, dic_ubg_to_vl):
        lessons_count = len(all_lessons)
        for i in range(lessons_count-1):
            vl = all_lessons[i]
            if(vl['type'] == "000000000000021"):
                cleaned_id = re.sub("_\d+$", "", vl['id'])
                if(cleaned_id in dic_ubg_to_vl):
                    vl["base"] = dic_ubg_to_vl[cleaned_id]


if __name__ == "__main__":
    with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    enricher = Enricher(jsonObject)
    enricher.enrich()