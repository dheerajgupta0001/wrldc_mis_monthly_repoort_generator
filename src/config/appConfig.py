import json
import pandas as pd
from typing import List, Any
from src.typeDefs.config.appConfig import IConstituentConfig

constituentsMappings: List[IConstituentConfig] = []
constituentsMappingsRE: List[Any] = []
jsonConfig: dict = {}


def initConfigs():
    loadJsonConfig()
    loadConstituentsMappings()
    loadREConstituentsMappings()


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


def loadREConstituentsMappings(filePath='config.xlsx', sheetname='REconstituents'):
    global constituentsMappingsRE
    constituentsMappingsREDf = pd.read_excel(filePath, sheet_name=sheetname)
    constituentsMappingsRE = constituentsMappingsREDf.to_dict('records')
    return constituentsMappingsRE


def getJsonConfig() -> dict:
    global jsonConfig
    return jsonConfig


def getConstituentsMappings():
    global constituentsMappings
    return constituentsMappings


def getREConstituentsMappings():
    global constituentsMappingsRE
    return constituentsMappingsRE
