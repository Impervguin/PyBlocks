from baseFuncs import fillFormat, getData, splitPrefix, I3BARVARIABLES, fillJSON, returnJSON
from psutil import virtual_memory
from psutil._common import bytes2human

# special variables:
# used
# total
# available
# procentavailable
# procentused
# item

RAMVariables = {
    "template": "{{item}}",
    "format": "usedtotal"
}

LOW = 30
HIGH = 80


def getRAMInfo() -> dict:
    mem = virtual_memory()
    return {
        "procent": mem.used / mem.total * 100,
        "total": mem.total / 1024 ** 3,
        "used": mem.used / 1024 ** 3
    }


result = {}
RAM = getRAMInfo()

RAMBlockData = getData("ram")

data, variablesWithPrefix = splitPrefix(RAMBlockData)

RAMVariables.update(data)

if RAM["procent"] < LOW and "low" in variablesWithPrefix.keys():
    RAMVariables.update(variablesWithPrefix["low"])
elif RAM["procent"] > HIGH and "high" in variablesWithPrefix.keys():
    RAMVariables.update(variablesWithPrefix["high"])

RAMVariables["used"] = round(RAM["used"], 1)
RAMVariables["total"] = round(RAM["total"], 1)
RAMVariables["available"] = round(RAM["total"] - RAM["used"], 1)
RAMVariables["procent"] = round(RAM["procent"], 1)
RAMVariables["item"] = f'{RAMVariables["used"]}/{RAMVariables["total"]}'

RAMVariables["template"] = RAMVariables["template"].strip()

result["full_text"] = fillFormat(RAMVariables)

result = fillJSON(result, RAMVariables)  # filling json with i3bar parametres

returnJSON(result)

