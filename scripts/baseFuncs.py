import json
import os
from jinja2 import Template


def getData(section) -> dict:
    try:
        with open(os.path.join(os.path.dirname(__file__), "data.json"), "r", encoding="utf-8") as f:
            d = json.load(f)
        return d[section]
    except KeyError:
        return dict()


def splitPrefix(rawData) -> tuple:
    variablesWithPrefix = dict()
    data = dict()
    for key in rawData.keys():
        if "!" in key:
            prefix, *other, name = key.split("!")
            if prefix not in variablesWithPrefix.keys():
                variablesWithPrefix[prefix] = dict()
            variablesWithPrefix[prefix][name] = rawData[key]
        else:
            data[key] = rawData[key]
    return data, variablesWithPrefix


def fillFormat(itemData) -> str:
    template = Template(itemData["template"])
    return template.render(**itemData)


I3BARVARIABLES = [
    "full_text",
    "short_text",
    "color",
    "background",
    "border",
    "border_top",
    "border_right",
    "border_bottom",
    "border_left",
    "min_width",
    "align",
    "name",
    "instance",
    "urgent",
    "separator",
    "separator_block_width",
    "markup"
]


def fillJSON(json: dict, variables: dict):
    for elem in I3BARVARIABLES:
        if elem in variables.keys():
            json[elem] = variables[elem]
    return json
