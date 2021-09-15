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
        tmp = linksList['vorlesung']
        tmpId = tmp['id']
        if(not tmpId in lessonIds):
            lessonIds.append(tmpId)
            lessonList.append(tmp)
    else:
        for links in linksList['links']:
            flatList(links, lessonList, lessonIds)


with open("linkList.json") as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

lessonList=[]
lessonIds=[]

flatList(jsonObject, lessonList, lessonIds)
print(f"{len(lessonIds)} verschiedene Vorlesungen geflatted")

i=0
zur=[]
for lesson in lessonList:
    for tmp in lesson['time']:
        tmp['slot'] = calcSlot(tmp)
    if(len(lesson['time']) == 0 ):
        print(f"{lesson['type']} : {VL_TYPE[lesson['type']]} : {lesson['id']}")
    i +=1

with open('dataTmp.json', 'w') as outfile:
    json.dump( lessonList, outfile, indent=2)

print(f"total ",i)


# 000000000000003 : Proseminar : 66-510
# 000000000000003 : Proseminar : 66-524
# 000000000000003 : Proseminar : 66-530
# 000000000000003 : Proseminar : 66-532
# 000000000000016 : Tutorium : 66-103
# 000000000000016 : Tutorium : 65-804
# 000000000000016 : Tutorium : 66-113
# 000000000000016 : Tutorium : 66-132
# 000000000000016 : Tutorium : 66-173
# 000000000000016 : Tutorium : 65-814
# 000000000000020 : Seminar : 66-651
# 000000000000021 : Übung : 65-802
# 000000000000021 : Übung : 65-812
# 000000000000021 : Übung : 66-102
# 000000000000021 : Übung : 66-112
# 000000000000021 : Übung : 66-131
# 000000000000021 : Übung : 66-151
# 000000000000021 : Übung : 66-171
# 000000000000021 : Übung : 66-191
# 000000000000021 : Übung : 66-904
# 000000000000021 : Übung : 66-902
# 000000000000023 : Praktikum : 66-120
# 000000000000023 : Praktikum : 66-121
# 000000000000023 : Praktikum : 66-122
# 000000000000023 : Praktikum : 66-123
# 000000000000023 : Praktikum : 66-455
# 000000000000023 : Praktikum : 66-677
# 000000000000026 : Begleitseminar : 66-456
# 000000000000047 : Fachtutorium : 66-860
# 000000000000047 : Fachtutorium : 66-874
# 000000000000053 : OE : 66-005
# 000000000000059 : Seminar/Übung : 66-658
# 000000000000077 : Anleitung : 65-806
# 000000000000077 : Anleitung : 65-816