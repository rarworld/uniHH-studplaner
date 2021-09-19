#! /usr/bin/env python3

import json

def clean_data(working_json):
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
            return_json['submenu'].append(clean_data(link))
    return return_json


def prepare_data(file_type):
    with open("linkList_"+file_type+".json") as jsonFile:
        json_object = json.load(jsonFile)
        jsonFile.close()

    start_obj = json_object

    return clean_data(start_obj)


if __name__ == '__main__':
    res = []
    res.append(prepare_data('Phy'))
    #res.append(prepare_data('Inf'))

    with open(f"nav.json", 'w') as outfile:
        json.dump( res, outfile, indent=2)