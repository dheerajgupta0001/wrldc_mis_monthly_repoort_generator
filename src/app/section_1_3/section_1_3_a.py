from src.typeDefs.aggregateMonthlyDataRecord import IAggregateDataRecord
import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.utils.getPrevFinYrDt import getPrevFinYrDt,getFinYrDt
import pandas as pd
from src.config.appConfig import getConstituentsMappings
import numpy as np
from src.typeDefs.section_1_3.section_1_3_a import ISection_1_3_a


def fetchSection1_3_aContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_3_a:
    constituentsInfos = getConstituentsMappings()

    constConfig = {}
    for c in constituentsInfos:
        constConfig[c["entity_tag"]] = c["display_name"]

    dataRecords = pd.DataFrame()
    mRepo = MetricsDataRepo(appDbConnStr)
    prevFinYrStartDt = getPrevFinYrDt(startDt)
    # get WR Unrestricted demand hourly values for this month and prev yr month
    allEntityReqMuVals = mRepo.getAllEntityMetricMonthlyData(
        'Requirement (MU)', startDt, endDt)
    allEntityAvailMuVals = mRepo.getAllEntityMetricMonthlyData(
        'Consumption(MU)', startDt, endDt)

    allEntityReqMuDf = pd.DataFrame(allEntityReqMuVals)
    allEntityAvailMuDf = pd.DataFrame(allEntityAvailMuVals)
    allEntityAvailMuDf = allEntityAvailMuDf.rename(columns={
        'metric_value': 'Consumption(MU)'})
    allEntityReqMuDf = allEntityReqMuDf.rename(columns={
        'metric_value': 'Requirement (MU)'})
    tempList = allEntityAvailMuDf['Consumption(MU)']
    allEntityReqMuDf['Consumption(MU)'] = tempList

    allEntityReqMuDf['shortage'] = round(100 *
                                         (allEntityReqMuDf['Requirement (MU)'] -
                                          allEntityReqMuDf['Consumption(MU)']) /
                                         allEntityReqMuDf['Consumption(MU)'], 2)
    # print(allEntityReqMuDf)

    prevYrAllEntityReqMuVals = mRepo.getAllEntityMetricMonthlyData(
        'Requirement (MU)', prevFinYrStartDt, endDt)
    prevYrAllEntityAvailMuVals = mRepo.getAllEntityMetricMonthlyData(
        'Consumption(MU)', prevFinYrStartDt, endDt)

    prevYrAllEntityReqMuDf = pd.DataFrame(prevYrAllEntityReqMuVals)
    prevYrAllEntityAvailMuDf = pd.DataFrame(prevYrAllEntityAvailMuVals)
    prevYrAllEntityAvailMuDf = prevYrAllEntityAvailMuDf.rename(columns={
        'metric_value': 'Consumption(MU)'})
    prevYrAllEntityReqMuDf = prevYrAllEntityReqMuDf.rename(columns={
        'metric_value': 'Requirement (MU)'})
    tempList = prevYrAllEntityAvailMuDf['Consumption(MU)']
    prevYrAllEntityReqMuDf['Consumption(MU)'] = tempList

    prevYrAllEntityReqMuDf['shortage'] = round(100 *
                                               (prevYrAllEntityReqMuDf['Requirement (MU)'] -
                                                prevYrAllEntityAvailMuDf['Consumption(MU)']) /
                                               prevYrAllEntityAvailMuDf['Consumption(MU)'], 2)
    prevYrAllEntityReqMuDf.set_index('entity_tag')
    dataRecords = pd.merge(
        allEntityReqMuDf, prevYrAllEntityReqMuDf, on='entity_tag')

    newNames = []
    for rIter in range(dataRecords.shape[0]):
        row = dataRecords.iloc[rIter, :]
        if row['entity_tag'] in constConfig:
            newNames.append(constConfig[row['entity_tag']])
        else:
            newNames.append(np.nan)
    dataRecords['entity_tag'] = newNames

    energyReqAvailList: ISection_1_3_a["energy_req_avail"] = []

    for i in dataRecords.index:
        energyReq: ISection_1_3_a = {
            'entity': dataRecords['entity_tag'][i],
            'reqMu_X': round(dataRecords['Requirement (MU)_x'][i]),
            'availMu_X': round(dataRecords['Consumption(MU)_x'][i]),
            'shortage_X': round(dataRecords['shortage_x'][i], 2),
            'reqMu_Y': round(dataRecords['Requirement (MU)_y'][i]),
            'availMu_Y': round(dataRecords['Consumption(MU)_y'][i]),
            'shortage_Y': round(dataRecords['shortage_y'][i], 2)
        }
        energyReqAvailList.append(energyReq)
    
    prevFinYrDateStr = dt.datetime.strftime(prevFinYrStartDt, "%b %y")
    sectionData: ISection_1_3_a = {
        "energy_req_avail": energyReqAvailList,
        "recent_fin_month_name": prevFinYrDateStr
    }

    return sectionData
