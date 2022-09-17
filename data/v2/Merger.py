#! /usr/bin/env python3

import json
import datetime

class Merger:

    def __init__(self, main_config) -> None:
        self.config = main_config['merger']
        self.debug = self.config['debug']
        self.studiengange = main_config['studiengange']
    

    def merging(self) -> json:
        data_json = {
            'file': self.config['file_name'],
            'exported': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'input_files': [],
            'data': []
        }
        self.__merge_studiengang(data_json)
        return data_json


    def __merge_studiengang(self, data_json):
        merged_lessions={}
        imported_files= data_json['input_files']

        for gang in self.studiengange:
            imported_files.append(self.__load_file_into_dic(merged_lessions, self.config['input_prefix'] + gang['short'] + ".json"))

        lesson_list=[]
        for k in merged_lessions:
            lesson_list.append(k)
        lesson_list.sort()

        export=[]
        for k in lesson_list:
            export.append(merged_lessions[k])

        data_json['data'] = export

        with open(data_json['file'], 'w') as outfile:
            json.dump( data_json, outfile, indent=2)

        print(f"total {len(lesson_list)}")


    def __load_studiengang_data(self, filename):
        with open(filename) as json_file:
            json_object = json.load(json_file)
            json_file.close()
        return json_object


    def __load_file_into_dic(self, dict, filename):
        input_object = self.__load_studiengang_data(filename)
        
        for vorl in input_object['data']:
            dict[vorl['id']] = vorl
        
        return {
            'name': input_object['name'],
            'parsed': input_object['parsed']
        }    


if __name__ == "__main__":
    with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    merger = Merger(jsonObject)
    merger.merging()