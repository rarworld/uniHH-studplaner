#! /usr/bin/env python3

import json
import re
from datetime import datetime,time
s1 = '10:33:26'
s2 = '11:15:49' # for example
FMT = '%H:%M:%S'
tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)


DAY_TO_NUMBER = {
    "Mo" : 0,
    "Di" : 1,
    "Mi" : 2,
    "Do" : 3,
    "Fr" : 4
}
FMT = '%H:%M'
TIME_SLOTS = [
     (time(8,0,0),0),
     (time(10,0,0),1),
     (time(12,0,0),2),
     (time(14,0,0),3),
     (time(16,0,0),4),
     (time(18,0,0),5)
]
VL_TYPE = {
    "000000000000001" : "Einführungsvorlesung", 
    "000000000000003" : "Proseminar", 
    "000000000000009" : "Einführungskurs", 
    "000000000000016" : "Tutorium", 
    "000000000000020" : "Seminar", 
    "000000000000021" : "Übung", 
    "000000000000022" : "Vorlesung",
    "000000000000023" : "Praktikum", 
    "000000000000024" : "Projekt", 
    "000000000000026" : "Begleitseminar", 
    "000000000000047" : "Fachtutorium", 
    "000000000000053" : "OE",
    "000000000000059" : "Seminar/Übung",
    "000000000000077" : "Anleitung" 
}


def calcSlot(timeJson):
    day = timeJson['day']
    startTime = datetime.strptime(timeJson['start'], FMT)
    res=-1
    for ts in TIME_SLOTS:
        if ts[0] <= startTime.time():
            res = ts[1]
    
    return (res, DAY_TO_NUMBER[day])

def flatList(linksList, lessonList, lessonIds):
    # print(linksList['name'])
    if(len(linksList['links'])==0):
        if 'vorlesung' in linksList:
            for tmp in linksList['vorlesung']:
                tmpId = tmp['id']
                if(not tmpId in lessonIds):
                    lessonIds.append(tmpId)
                    lessonList.append(tmp)
    else:
        for links in linksList['links']:
            flatList(links, lessonList, lessonIds)


def prepareData(fileType):
    with open("linkList_"+fileType+".json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    lessonList=[]
    lessonIds=[]

    flatList(jsonObject, lessonList, lessonIds)
    print(f"{len(lessonList)} verschiedene Vorlesungen geflatted")

    i=0
    empty_count=0
    for lesson in lessonList:
        if not('time' in lesson) or len(lesson['time']) == 0 :
            if not ('blub' in lesson):
                print(f"{lesson['type']} : {VL_TYPE[lesson['type']]} : {lesson['id']}")
            else:
                print(f"{lesson['type']} : {VL_TYPE[lesson['type']]} : {lesson['id']} {lesson['blub']}")
                empty_count += 1
        else:
            for tmp in lesson['time']:
                tmp['slot'] = calcSlot(tmp)
            i +=1

    with open(f"data{fileType}.json", 'w') as outfile:
        json.dump( lessonList, outfile, indent=2)

    print(f"Exported ",i)
    print(f"Empty ", empty_count)
    print(f"Missing ", (len(lessonList) - i - empty_count))


if __name__ == '__main__':
    prepareData('Phy')
    prepareData('Inf')
    #prepareData('Tmp')


# prepareData('Phy')
#  - 142 verschiedene Vorlesungen geflatted
#  - Exported  106
#  - Empty  34
#  - Missing  2
#
# prepareData('Inf')
#  - 204 verschiedene Vorlesungen geflatted
#  - Exported  176
#  - Empty  25
#  - Missing  3
#  Totalmissing 5 von 346
# 
#
# 16 : Tutorium : 65-814_0
# 16 : Tutorium : 65-814_1
# 
# 16 : Tutorium : 65-814_0
# 16 : Tutorium : 65-814_1
# 21 : Übung : 64-041_16