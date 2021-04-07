
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
import math
import matplotlib.pyplot as plt
from src.utils.convertDtToDayNum import convertDtToDayNum



def fetchSection1_13Context(appDbConnStr:str, filePath: str, startDt: dt.datetime, endDt: dt.datetime):
   
    mRepo = MetricsDataRepo(appDbConnStr)
   
    allRecords = mRepo.getRRASData(filePath , startDt , endDt)
    
    upRecords = allRecords['up']
    downRecords = allRecords['down']


    sectionData = {}

    sectionData['rrasUp'] = CreateListUP(upRecords)
    sectionData['rrasDown'] = CreateListDown(downRecords)

    
    return sectionData

def CreateListUP(records) -> list:
    length = len(records)
    array = []
    for itr in range(length):
        obj = {}
        obj['Name'] = records.iloc[itr,0]
        obj['mwh'] = records.iloc[itr,1]
        obj['mw'] = records.iloc[itr,2]
        obj['fixed'] = records.iloc[itr,3]
        obj['variable'] = records.iloc[itr,4]
        obj['markup'] = records.iloc[itr,5]
        obj['total'] = records.iloc[itr,6]

        array.append(obj)
    
    return array

def CreateListDown(records) -> list:
    length = len(records)
    array = []
    for itr in range(length):
        obj = {}
        obj['Name'] = records.iloc[itr,0]
        obj['mwh'] = records.iloc[itr,1]
        obj['mw'] = records.iloc[itr,2]
        obj['variable'] = records.iloc[itr,3]
        obj['dsm'] = records.iloc[itr,4]
        

        array.append(obj)
    
    return array