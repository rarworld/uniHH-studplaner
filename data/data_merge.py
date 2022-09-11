#! /usr/bin/env python3

import json
import datetime

def load_file_into_dic(dict, urlPath):
    with open(urlPath) as jsonFile:
        json_object = json.load(jsonFile)
        jsonFile.close()
    
    for vorl in json_object['data']:
        dict[vorl['id']] = vorl
    
    return {
        'name': json_object['name'],
        'parsed': json_object['parsed']
    }


if __name__ == '__main__':
    dict={}
    imported_files=[]

    imported_files.append(load_file_into_dic(dict, "data"+"Inf"+".json"))
    imported_files.append(load_file_into_dic(dict, "data"+"Phy"+".json"))

    lessonList=[]
    for k in dict:
        lessonList.append(k)
    lessonList.sort()

    export=[]
    for k in lessonList:
        export.append(dict[k])

    exportDate = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    result = {
        'exported': exportDate,
        'files': imported_files,
        'data': export
    }

    with open("data.json", 'w') as outfile:
        json.dump( result, outfile, indent=2)

    print(f"total ",len(lessonList))
