#! /usr/bin/env python3

from datetime import datetime,time
import json

class Preparer:

    DAY_TO_NUMBER = {
        "Mo" : 0,
        "Di" : 1,
        "Mi" : 2,
        "Do" : 3,
        "Fr" : 4,
        "Sa" : 5,
        "So" : 6
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

    def __init__(self, main_config) -> None:
        self.config = main_config['preparer']
        self.debug = self.config['debug']
        self.studiengange = main_config['studiengange']
    

    def preparing(self):
        for gang in self.studiengange:
            print(f"preparing {gang['name']}")
            overview_json = self.prepare_studiengang(gang)
            with open(overview_json['file'], 'w') as outfile:
                json.dump( overview_json, outfile, indent=2)


    def prepare_studiengang(self, studiengang) -> json:
        data_json = {
            'file': self.config['file_name_prefix'] + studiengang['short'] + ".json",
            'name': studiengang['name'],
            'input': self.config['input_prefix'] + studiengang['short'] + ".json",
            'parsed': "",
            'data': []
        }
        self.__prepare_data(data_json)
        return data_json


    def __open_link_list(self, filename):
        with open(filename) as json_file:
            json_object = json.load(json_file)
            json_file.close()
        return json_object


    def __prepare_data(self, data_json):
        input_object = self.__open_link_list(data_json['input'])

        data_json['parsed'] = input_object['date']
        lesson_list=data_json['data']
        lesson_ids=[]

        self.__flat_list(input_object, lesson_list, lesson_ids)
        print(f"{len(lesson_list)} verschiedene Vorlesungen geflatted")

        i=0
        empty_count=0
        for lesson in lesson_list:
            if ('time' not in lesson) or len(lesson['time']) == 0 :
                if ('blub' not in lesson):
                    print(f"{lesson['type']} : {self.VL_TYPE[lesson['type']]} : {lesson['id']}")
                else:
                    print(f"{lesson['type']} : {self.VL_TYPE[lesson['type']]} : {lesson['id']} {lesson['blub']}")
                    empty_count += 1
            else:
                for tmp in lesson['time']:
                    tmp['slot'] = self.__calc_slot(tmp)
                i +=1

        with open(data_json['file'], 'w') as outfile:
            json.dump( data_json, outfile, indent=2)

        if(self.debug):
            print(f"Exported ",i)
            print(f"Empty ", empty_count)
            print(f"Missing ", (len(lesson_list) - i - empty_count))


    def __flat_list(self, linksList, lesson_list, lesson_ids):
        if(len(linksList['links'])==0):
            if 'vorlesung' in linksList:
                for tmp in linksList['vorlesung']:
                    tmp_id = tmp['id']
                    if(tmp_id not in lesson_ids):
                        lesson_ids.append(tmp_id)
                        lesson_list.append(tmp)
        else:
            for links in linksList['links']:
                self.__flat_list(links, lesson_list, lesson_ids)


    def __calc_slot(self, timeJson):
        day = timeJson['day']
        start_time = datetime.strptime(timeJson['start'], self.FMT)
        res=-1
        for ts in self.TIME_SLOTS:
            if ts[0] <= start_time.time():
                res = ts[1]
        
        return (res, self.DAY_TO_NUMBER[day])


if __name__ == "__main__":
    with open("config.json") as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()

    preparer = Preparer(jsonObject)
    preparer.preparing()