import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.config.appConfig import getVoltMetrics
import numpy as np
from src.typeDefs.section_1_7.section_1_7 import ISection_1_7, IVoltageRecord


def fetchSection1_7Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_7:
    metricsInfo = getVoltMetrics()
    mRepo = MetricsDataRepo(appDbConnStr)

    allMetricDf :pd.DataFrame = []


    for metricIndex in range(len(metricsInfo)):
        metricInfo = metricsInfo[metricIndex]

        voltLevel = metricInfo['voltageLevel']
        operation = metricInfo['operation']
        metricName = metricInfo['metric_name']
        
        if operation is not 'compute':
            allEntityMetricData = mRepo.getDailyVoltDataByLevel(voltLevel,metricName ,startDt,endDt)
            
            allEntityMetricDf = allEntityMetricData.pivot(
                index='entity_name', columns='metric_name', values='data_val')
            allEntityMetricDf.reset_index(inplace=True)
            allEntityMetricDf = allEntityMetricDf.groupby("entity_name")

            if operation == 'sum':
                allEntityMetricDf['val'] = allEntityMetricDf['data_val'].sum()
            elif operation == 'max':
                allEntityMetricDf['val'] = allEntityMetricDf['data_val'].max()
            elif operation == 'min':
                allEntityMetricData['val'] = allEntityMetricData['dala_val'].min()
            
            allMetricDf[metricName] = allEntityMetricDf['val']

        else:
            refColumnName = metricInfo['evalColumn']
            multiplyFactor = metricInfo['multiply']

            if multiplyFactor == 'monthHrs':
                difference = endDt - startDt
                days = difference.days
                factor = days * 24

            elif multiplyFactor == 'weekHrs':
                factor = 24*7

            allMetricDf[metricName] =  allMetricDf[refColumnName] * factor



    allMetricRecords :IVoltageRecord = allMetricDf.to_dict('records')
    secData:ISection_1_7 = {
        'voltageLevel': allMetricRecords
    }
    
    return secData
