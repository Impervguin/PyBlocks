import os
from baseFuncs import fillFormat, getData, splitPrefix, I3BARVARIABLES, fillJSON, returnJSON
from math import ceil

# available prefixes:
# charging

# path to battery files via sysfs
BATTERYPATH = "/sys/class/power_supply/BAT0"

# default values
batteryVariables = {"marking-icon": "■",
                    "empty-icon": "_",
                    "marking-count": 5,
                    "template": "{{item}}"
                    }


def getBatteryInfo() -> dict:  # getting info about current state of battery
    batteryInfo = dict()
    with open(os.path.join(BATTERYPATH, "capacity"), 'r', encoding="utf-8") as file:
        batteryInfo["capacity"] = int(file.readline().strip())

    with open(os.path.join(BATTERYPATH, "status"), 'r', encoding="utf-8") as file:
        batteryInfo["status"] = file.readline().strip()

    return batteryInfo


result = dict()

batteryInfo = getBatteryInfo()

batteryBlockData = getData("battery-cubics")  # getting custom variables from data.ini

data, variablesWithPrefix = splitPrefix(batteryBlockData)  # split variables by prefix

batteryVariables.update(data)  # replace base values with custom

if batteryInfo['status'] in ("Charging", "Full") and "charging" in variablesWithPrefix.keys():
    batteryVariables.update(variablesWithPrefix["charging"])  # replace variables with prefix ones

if not isinstance(batteryVariables["marking-count"], int):
    batteryVariables["marking-count"] = int(batteryVariables["marking-count"])
batteryVariables["template"] = batteryVariables["template"].strip()

batteryCapacity = ceil(
    batteryInfo["capacity"] / (100 / batteryVariables["marking-count"]))  # counting how much markings are filled
item = batteryCapacity * batteryVariables["marking-icon"] + (batteryVariables["marking-count"] - batteryCapacity) * \
       batteryVariables[
           "empty-icon"]  # creating the main item of block
batteryVariables["item"] = item

result["full_text"] = fillFormat(batteryVariables)

result = fillJSON(result, batteryVariables)  # filling json with i3bar parametres

returnJSON(result)  # returning result in json
