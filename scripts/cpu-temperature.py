from baseFuncs import fillFormat, getData, splitPrefix, I3BARVARIABLES, fillJSON, returnJSON
from psutil import sensors_temperatures
import os

CPUTempVariables = {
    "template": "{{item}}"
}

SENSORNAME = "k10temp"

HIGH = 70
LOW = 40

def getCPUTempInfo() -> float:
    return round(sensors_temperatures()[SENSORNAME][0].current)

result = {}
CPUTemp = getCPUTempInfo()

CPUBlockData = getData("cpu-temp")

data, variablesWithPrefix = splitPrefix(CPUBlockData)

CPUTempVariables.update(data)

if CPUTemp < LOW and "low" in variablesWithPrefix.keys():
    CPUTempVariables.update(variablesWithPrefix["low"])
elif CPUTemp > HIGH and "high" in variablesWithPrefix.keys():
    CPUTempVariables.update(variablesWithPrefix["high"])

CPUTempVariables["template"] = CPUTempVariables["template"].strip()

CPUTempVariables["item"] = CPUTemp

result["full_text"] = fillFormat(CPUTempVariables)

result = fillJSON(result, CPUTempVariables)  # filling json with i3bar parametres

returnJSON(result)