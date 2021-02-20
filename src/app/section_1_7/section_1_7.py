import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.config.appConfig import getVoltMetrics
import numpy as np
from src.typeDefs.section_1_7.section_1_7 import ISection_1_7, IVoltageRecord
import math
from typing import List

def fetchSection1_7Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_7:
    metricsInfo = getVoltMetrics()
    mRepo = MetricsDataRepo(appDbConnStr)

    allMetris  = {}
    allMetris['400'] = {}
    allMetris['765'] = {}

    allStations = []

    for metricIndex in range(len(metricsInfo)):
        metricInfo = metricsInfo[metricIndex]

        voltLevel = metricInfo['voltageLevel']
        operation = metricInfo['operation']
        metricName = metricInfo['metric_name']
        
        if operation != 'compute ':
            allEntityMetricData = mRepo.getDailyVoltDataByLevel(voltLevel,metricName ,startDt,endDt)
            allEntityMetricDf = pd.DataFrame(allEntityMetricData)
            allEntityMetricDf = allEntityMetricDf.groupby("entity_name")
            allStations = allEntityMetricDf.groups.keys()
            combinedObj = {}

            for eachStation in allStations:
                combinedObj[eachStation] = []

            for eachRecord in allEntityMetricData:
                if math.isnan(float(eachRecord['data_val'])):
                    eachRecord['data_val'] = 0
                combinedObj[eachRecord['entity_name']].append(float(eachRecord['data_val']))

            stndWiseOperationData = {}
            for eachStation in allStations:
                stnData = combinedObj[eachStation]
                val = 0
                if operation == 'max':
                    val = max(stnData)
                
                elif operation == 'sum':
                    val = sum(stnData) / ((endDt - startDt).days +1)
                    # val = sum(stnData)

                
                elif operation == 'min':
                    val = min(stnData)

                stndWiseOperationData[eachStation] = val
            

            allMetris[str(voltLevel)][metricName] = stndWiseOperationData
            
        
        else:
            refColumnName = metricInfo['evalColumn']
            multiplyFactor = metricInfo['multiply']
            allMetris[metricName] = {}

            stndWiseOperationData = {}


            for eachStation in allStations:
                val = allMetris[str(voltLevel)][refColumnName][eachStation]

                if multiplyFactor == 'monthHrs':
                    difference = endDt - startDt
                    days = difference.days + 1
                    factor = days * 24
                    stndWiseOperationData[eachStation] = int(val) * factor


                elif multiplyFactor == 'weekHrs':
                    factor = 24*7
                    stndWiseOperationData[eachStation] = int(val) / factor



            allMetris[str(voltLevel)][metricName] = stndWiseOperationData

            

        
    print(allMetris)

    df400 = pd.DataFrame(allMetris['400'])
    df765 = pd.DataFrame(allMetris['765'])

    df = df765.append(df400, ignore_index=True)
    allMetricRecords400KV :List[IVoltageRecord] = []
    allMetricRecords765V :List[IVoltageRecord] = []

    allMetricRecords400KV = builtIRecord(df400)
    allMetricRecords765V = builtIRecord(df765)
        
    
    secData:ISection_1_7 = {
        'voltageLevel400KV': allMetricRecords400KV , 
        'voltageLevel765KV': allMetricRecords765V
    }
    
    return secData


def builtIRecord(df) -> List[IVoltageRecord]:
    metricRecords :List[IVoltageRecord] = []
    for i in df.index:
        voltageRecord:IVoltageRecord = {
            'Name':i , 
            'Max':df['Max'][i] ,
            'Min':df['Min'][i] ,
            '%Time <380 or 728': df['%Time <380 or 728'][i] ,
            '%Time within IEGC Band': df['%Time within IEGC Band'][i] ,
            '%Time >420 or 800': df['%Time >420 or 800'][i] ,
            'Hrs Below 728':df['Hrs Below 728'][i] ,
            'Hrs Above 800': df['Hrs Above 800'][i] ,
            'Hrs Outside IEGC Band(VDI)':df['Hrs Outside IEGC Band(VDI)'][i] ,
            'vdi': df['vdi'][i] , 
            'Hrs Below 370':df['Hrs Below 370'][i] , 
            'Hrs Above 420':df['Hrs Above 420'][i] 

        }
        metricRecords.append(voltageRecord)
    return metricRecords
