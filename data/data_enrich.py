#! /usr/bin/env python3

import json
import datetime
import re

def load_data_file(urlPath):
    with open(urlPath) as jsonFile:
        json_object = json.load(jsonFile)
        jsonFile.close()

    return json_object


def add_ubg_to_vl(all_lessons):
    lessons_count = len(all_lessons)
    ubg_vl_dict = {}

    for i in range(lessons_count-1):
        vl = all_lessons[i]
        if( 'short' in vl and vl['short'] != "" ):
            if(vl['type'] == "000000000000022"):
                ubg = all_lessons[i+1]
                if(ubg['type'] == "000000000000021"):
                    vl_clean_name = vl['name'].replace("Vorlesung ","").lower()
                    if( vl_clean_name in ubg['name'].lower() ):
                        ubg_vl_dict[ubg['id']]=vl['id']
                        vl["base"] = ubg['id']
    
    return ubg_vl_dict

def add_vl_to_ubg(all_lessons, dic_ubg_to_vl):
    lessons_count = len(all_lessons)
    for i in range(lessons_count-1):
        vl = all_lessons[i]
        if(vl['type'] == "000000000000021"):
            cleaned_id = re.sub("_\d+$", "", vl['id'])
            if(cleaned_id in dic_ubg_to_vl):
                vl["base"] = dic_ubg_to_vl[cleaned_id]



if __name__ == '__main__':
    data = load_data_file("data.json")

    # Enrich Vorlesung with Ubungs-id
    ubg_vl_dict = add_ubg_to_vl(data['data'])
    add_vl_to_ubg(data['data'], ubg_vl_dict)

    with open("data_enriched.json", 'w') as outfile:
        json.dump( data, outfile, indent=2)



