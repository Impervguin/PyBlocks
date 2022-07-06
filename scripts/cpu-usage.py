from baseFuncs import fillFormat, getData, splitPrefix, I3BARVARIABLES, fillJSON, returnJSON
from psutil import cpu_times_percent
import os

CPUUsageVariables = {
    "template": "{{item}}"
}


HIGH = 70
LOW = 10

def getCPUUsageInfo() -> float:
    return round(100 - cpu_times_percent(interval=1)[3], 1)

result = {}
CPUUsage = getCPUUsageInfo()

CPUBlockData = getData("cpu-usage")

data, variablesWithPrefix = splitPrefix(CPUBlockData)

CPUUsageVariables.update(data)

if CPUUsage <= LOW and "low" in variablesWithPrefix.keys():
    CPUUsageVariables.update(variablesWithPrefix["low"])
elif CPUUsage >= HIGH and "high" in variablesWithPrefix.keys():
    CPUUsageVariables.update(variablesWithPrefix["high"])

CPUUsageVariables["template"] = CPUUsageVariables["template"].strip()

CPUUsageVariables["item"] = CPUUsage

result["full_text"] = fillFormat(CPUUsageVariables)

result = fillJSON(result, CPUUsageVariables)  # filling json with i3bar parametres

returnJSON(result)
