import os
from baseFuncs import fillFormat, getData, splitPrefix, I3BARVARIABLES

# available prefixes:
# charging
# battery0
# battery20
# battery50
# battery80
# battery100


# path to battery files via sysfs
BATTERYPATH = "/sys/class/power_supply/BAT0"

# default values
batteryVariables = {
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

try:
    batteryInfo = getBatteryInfo()
except BaseException as e:
    print("Failed to get battery info")
    exit()

batteryBlockData = getData("battery-icons")  # getting custom variables from data.ini

data, variablesWithPrefix = splitPrefix(batteryBlockData)  # split variables by prefix

for key in data:
    batteryVariables[key] = data[key]  # replace base values with custom

# replace variables with prefix ones
if 80 < batteryInfo["capacity"] <= 100 and "battery80" in variablesWithPrefix:
    for key in variablesWithPrefix["battery80"].keys():
        batteryVariables[key] = variablesWithPrefix["battery80"][key]
elif 50 < batteryInfo["capacity"] <= 80 and "battery50" in variablesWithPrefix:
    for key in variablesWithPrefix["battery50"].keys():
        batteryVariables[key] = variablesWithPrefix["battery50"][key]
elif 20 < batteryInfo["capacity"] <= 50 and "battery20" in variablesWithPrefix:
    for key in variablesWithPrefix["battery20"].keys():
        batteryVariables[key] = variablesWithPrefix["battery20"][key]
elif 0 < batteryInfo["capacity"] <= 20 and "battery0" in variablesWithPrefix:
    for key in variablesWithPrefix["battery0"].keys():
        batteryVariables[key] = variablesWithPrefix["battery0"][key]
elif batteryInfo['status'] == "Charging" and "charging" in variablesWithPrefix.keys():
    for key in variablesWithPrefix["charging"].keys():
        batteryVariables[key] = variablesWithPrefix["charging"][key]

batteryVariables["template"].strip()

item = str(batteryInfo["capacity"])
batteryVariables["item"] = item

result["full_text"] = fillFormat(batteryVariables)

for elem in I3BARVARIABLES:
    if elem in batteryVariables.keys():
        result[elem] = batteryVariables[elem]  # filling json with i3bar parametres

print(str(result).replace("'", '"'))  # returning result in json
