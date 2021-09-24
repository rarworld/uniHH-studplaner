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
    zur=[]
    for lesson in lessonList:
        if not('time' in lesson) or len(lesson['time']) == 0 :
            print(f"{lesson['type']} : {VL_TYPE[lesson['type']]} : {lesson['id']}")
        else:
            for tmp in lesson['time']:
                tmp['slot'] = calcSlot(tmp)
            i +=1

    with open(f"data{fileType}.json", 'w') as outfile:
        json.dump( lessonList, outfile, indent=2)

    print(f"Exported ",i)
    print(f"Missing ", (len(lessonList) - i))


if __name__ == '__main__':
    prepareData('Phy')
    prepareData('Inf')
    #prepareData('Tmp')

# prepareData('Phy')
#  - 142 verschiedene Vorlesungen geflatted
#  - Exported 106
#  - Missing 36
# prepareData('Inf')
#  - 204 verschiedene Vorlesungen geflatted
#  - Exported 176
#  - Missing 28
#
# Totalmissing 36+28 = 64 von 346
# 
# 53 : OE : 66-005
# 21 : Übung : 66-102
# 16 : Tutorium : 66-103
# 21 : Übung : 65-802
# 16 : Tutorium : 65-804
# 77 : Anleitung : 65-806
# 23 : Praktikum : 66-120
# 23 : Praktikum : 66-121
# 21 : Übung : 66-112
# 16 : Tutorium : 66-113
# 23 : Praktikum : 66-122
# 23 : Praktikum : 66-123
# 21 : Übung : 66-131
# 16 : Tutorium : 66-132
# 21 : Übung : 66-171
# 16 : Tutorium : 66-173
# 21 : Übung : 65-812
# 16 : Tutorium : 65-814
# 16 : Tutorium : 65-814_0
# 16 : Tutorium : 65-814_1
# 77 : Anleitung : 65-816
# 21 : Übung : 66-151
# 23 : Praktikum : 66-455
# 26 : Begleitseminar : 66-456
# 21 : Übung : 66-191
# 47 : Fachtutorium : 66-860
# 47 : Fachtutorium : 66-874
# 03 : Proseminar : 66-510
# 03 : Proseminar : 66-524
# 03 : Proseminar : 66-530
# 03 : Proseminar : 66-532
# 21 : Übung : 66-902
# 21 : Übung : 66-904
# 23 : Praktikum : 66-677
# 20 : Seminar : 66-651
# 59 : Seminar/Übung : 66-658
# 
# 21 : Übung : 67-101
# 21 : Übung : 64-071
# 21 : Übung : 64-081
# 21 : Übung : 65-802
# 16 : Tutorium : 65-804
# 77 : Anleitung : 65-806
# 21 : Übung : 65-072
# 24 : Projekt : 66-784
# 21 : Übung : 66-102
# 16 : Tutorium : 66-103
# 21 : Übung : 66-112
# 16 : Tutorium : 66-113
# 23 : Praktikum : 66-120
# 23 : Praktikum : 66-121
# 21 : Übung : 65-812
# 16 : Tutorium : 65-814
# 16 : Tutorium : 65-814_0
# 16 : Tutorium : 65-814_1
# 77 : Anleitung : 65-816
# 23 : Praktikum : 66-786
# 21 : Übung : 66-191
# 21 : Übung : 64-254
# 21 : Übung : 64-257
# 21 : Übung : 64-041
# 21 : Übung : 64-041_16
# 23 : Praktikum : 64-042
# 21 : Übung : 65-052
# 21 : Übung : 66-151