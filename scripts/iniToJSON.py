from configparser import ConfigParser
import json
import os


def iniToJSON(fName):
    configur = ConfigParser()
    configur.read(os.path.join(os.path.dirname(__file__), fName))
    try:
        Data = configur
        d = dict()
        for section in Data.keys():
            d[section] = {}
            for key in Data[section]:
                d[section][key] = Data[section][key]
        jsonName = fName[:-4] + ".json"
        with open(jsonName, "w", encoding="utf-8") as f:
            json.dump(d, f)
        print("Success!")
    except KeyError:
        return dict()

iniToJSON("data.ini")