#! /usr/bin/env python3

import json

def loadFileIntoDic(dict, urlPath):
    with open(urlPath) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    
    for vorl in jsonObject:
        dict[vorl['id']] = vorl


if __name__ == '__main__':
    dict={}

    loadFileIntoDic(dict, "data"+"Inf"+".json")
    loadFileIntoDic(dict, "data"+"Phy"+".json")

    lessonList=[]
    for k in dict:
        lessonList.append(dict[k])

    with open("data.json", 'w') as outfile:
        json.dump( lessonList, outfile, indent=2)

    print(f"total ",len(lessonList))
