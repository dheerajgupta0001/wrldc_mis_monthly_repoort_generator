import json
import pandas as pd
from typing import List, Any

constituentsMappings: List[Any] = []
voltMetrics: List[Any] = []
jsonConfig: dict = {}


def initConfigs():
    loadJsonConfig()
    loadConstituentsMappings()
    loadMetricsInfo()

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
    # fileMappings = fileMappingsDf.where(pd.notnull(fileMappings),None)
    constituentsMappings = constituentsMappingsDf.to_dict('records')
    return constituentsMappings

def loadMetricsInfo(filePath='config.xlsx', sheetname='volt_metrics'):
    global voltMetrics
    voltMetrics = pd.read_excel(filePath, sheet_name=sheetname)
    voltMetrics = voltMetrics.to_dict('records')
    return voltMetrics

def getJsonConfig() -> dict:
    global jsonConfig
    return jsonConfig

def getConstituentsMappings():
    global constituentsMappings
    return constituentsMappings

def getVoltMetrics():
    global voltMetrics
    return voltMetrics