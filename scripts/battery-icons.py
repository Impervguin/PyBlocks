import os
from baseFuncs import fillFormat, getData, splitPrefix, I3BARVARIABLES, fillJSON

# path to battery files via sysfs
BATTERYPATH = "/sys/class/power_supply/BAT0"

# default values
batteryVariables = {
    "template": "{{item}}"
}

HIGH = 70
LOW = 10

def getBatteryInfo() -> dict:  # getting info about current state of battery
    batteryInfo = dict()
    with open(os.path.join(BATTERYPATH, "capacity"), 'r', encoding="utf-8") as file:
        batteryInfo["capacity"] = int(file.readline().strip())

    with open(os.path.join(BATTERYPATH, "status"), 'r', encoding="utf-8") as file:
        batteryInfo["status"] = file.readline().strip()

    return batteryInfo


result = dict()

batteryInfo = getBatteryInfo()

batteryBlockData = getData("battery-icons")  # getting custom variables from data.ini

data, variablesWithPrefix = splitPrefix(batteryBlockData)  # split variables by prefix

batteryVariables.update(data)  # replace base values with custom
# replace variables with prefix ones
if batteryInfo['status'] == "Charging" and "charging" in variablesWithPrefix:
    batteryVariables.update(variablesWithPrefix["charging"])
elif batteryInfo["capacity"] == 100 and "full" in variablesWithPrefix:
    batteryVariables.update(variablesWithPrefix["full"])
elif 80 < batteryInfo["capacity"] < 100 and "battery80" in variablesWithPrefix:
    batteryVariables.update(variablesWithPrefix["battery80"])
elif 50 < batteryInfo["capacity"] <= 80 and "battery50" in variablesWithPrefix:
    batteryVariables.update(variablesWithPrefix["battery50"])
elif 20 < batteryInfo["capacity"] <= 50 and "battery20" in variablesWithPrefix:
    batteryVariables.update(variablesWithPrefix["battery20"])
elif 0 < batteryInfo["capacity"] <= 20 and "battery0" in variablesWithPrefix:
    batteryVariables.update(variablesWithPrefix["battery0"])

batteryVariables["template"].strip()

item = str(batteryInfo["capacity"])
batteryVariables["item"] = item

result["full_text"] = fillFormat(batteryVariables)

result = fillJSON(result, batteryVariables)  # filling json with i3bar parametres

print(str(result).replace("'", '"'))  # returning result in json
