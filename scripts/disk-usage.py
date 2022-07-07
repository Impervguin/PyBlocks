from baseFuncs import fillFormat, getData, splitPrefix, I3BARVARIABLES, fillJSON, returnJSON
from psutil import disk_usage

# special variables:
# used
# total
# available
# procentavailable
# procentused
# item

diskVariables = {
    "template": "{{item}}",
}

LOW = 30
HIGH = 80


def getDiskInfo() -> dict:
    mem = disk_usage("/")
    return {
        "procent": mem.percent,
        "total": mem.total / 1024 ** 3,
        "used": mem.used / 1024 ** 3,
        "free": mem.free / 1024**3
    }

result = {}
disk = getDiskInfo()

diskBlockData = getData("disk-usage")

data, variablesWithPrefix = splitPrefix(diskBlockData)

diskVariables.update(data)

if disk["procent"] < LOW and "low" in variablesWithPrefix.keys():
    diskVariables.update(variablesWithPrefix["low"])
elif disk["procent"] > HIGH and "high" in variablesWithPrefix.keys():
    diskVariables.update(variablesWithPrefix["high"])

diskVariables["used"] = round(disk["used"], 1)
diskVariables["total"] = round(disk["total"], 1)
diskVariables["available"] = round(disk["free"], 1)
diskVariables["procentused"] = round(disk["procent"], 1)
diskVariables["procentavailable"] = round(100 - disk["procent"], 1)
diskVariables["item"] = f'{diskVariables["available"]}/{diskVariables["total"]}'

diskVariables["template"] = diskVariables["template"].strip()

result["full_text"] = fillFormat(diskVariables)

result = fillJSON(result, diskVariables)  # filling json with i3bar parametres

returnJSON(result)