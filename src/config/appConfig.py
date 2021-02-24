import json
import pandas as pd
from typing import List, Any

constituentsMappings: List[Any] = []

jsonConfig: dict = {}


def initConfigs():
    loadJsonConfig()
    loadConstituentsMappings()
    loadReservoirsMappings()


def loadJsonConfig(fName="config.json") -> dict:
    global jsonConfig
    with open(fName) as f:
        data = json.load(f)
        jsonConfig = data
        return jsonConfig

def loadConstituentsMappings(filePath='config.xlsx', sheetname='constituents'):
    global constituentsMappings
    constituentsMappingsDf = pd.read_excel(filePath, sheet_name=sheetname)
    # Convert Nan to None
    constituentsMappings = constituentsMappingsDf.to_dict('records')
    return constituentsMappings

def loadReservoirsMappings(filePath='config.xlsx', sheetname='reservoir'):
    global reservoirsMappings
    reservoirsMappingsDf = pd.read_excel(filePath, sheet_name=sheetname)
    # Convert Nan to None
    reservoirsMappings = reservoirsMappingsDf.to_dict('records')
    return reservoirsMappings


def getJsonConfig() -> dict:
    global jsonConfig
    return jsonConfig

def getConstituentsMappings():
    global constituentsMappings
    return constituentsMappings

def getReservoirsMappings():
    global reservoirsMappings
    return reservoirsMappings