from src.typeDefs.aggregateMonthlyDataRecord import IAggregateDataRecord
import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.config.appConfig import getConstituentsMappings
import numpy as np
from src.typeDefs.section_1_3.section_1_3_b import ISection_1_3_b, ISoFarHighestDataRow


def fetchSection1_3_bContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_3_b:
    constituentsInfos = getConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    soFarHighestAllEntityReqVals = mRepo.getSoFarHighestAllEntityData(
        'soFarHighestRequirement', addMonths(startDt, -1))
    soFarHighestReqLookUp = {}
    for v in soFarHighestAllEntityReqVals:
        soFarHighestReqLookUp[v['constituent']] = {
            'value': v['data_value'], 'ts': v['data_time']}

    soFarHighestAllEntityAvailVals = mRepo.getSoFarHighestAllEntityData(
        'soFarHighestAvailability', addMonths(startDt, -1))
    soFarHighestAvailLookUp = {}
    for v in soFarHighestAllEntityAvailVals:
        soFarHighestAvailLookUp[v['constituent']] = {
            'value': v['data_value'], 'ts': v['data_time']}
    dispRows: List[ISoFarHighestDataRow] = []
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]
        availData = mRepo.getEntityMetricHourlyData(
            constInfo["entity_tag"], "Demand(MW)", startDt, endDt)
        loadSheddingData = mRepo.getEntityMetricHourlyData(
            constInfo["entity_tag"], "Load Shedding(MW)", startDt, endDt)
        availReqData = availData + loadSheddingData
        availReqDataDf = pd.DataFrame(availReqData)
        availReqDataDf = availReqDataDf.pivot(
            index='time_stamp', columns='metric_name', values='data_value')
        availReqDataDf.reset_index(inplace=True)
        availReqDataDf["Requirement"] = availReqDataDf["Demand(MW)"] + \
            availReqDataDf["Load Shedding(MW)"]
        maxReq = availReqDataDf["Requirement"].max()
        maxReqDt = availReqDataDf["time_stamp"].loc[availReqDataDf["Requirement"].idxmax(
        )]
        maxAvail = availReqDataDf["Demand(MW)"].max()
        maxAvailDt = availReqDataDf["time_stamp"].loc[availReqDataDf["Demand(MW)"].idxmax(
        )]
        maxShortagePerc = round(100*(maxReq-maxAvail)/maxAvail, 2)

        prevHighestReqObj = soFarHighestReqLookUp[constInfo["entity_tag"]]
        newHighestReq = maxReq
        newHighestReqTime = maxReqDt.to_pydatetime()
        if newHighestReq < prevHighestReqObj["value"]:
            newHighestReq = prevHighestReqObj["value"]
            newHighestReqTime = prevHighestReqObj["ts"]

        prevHighestAvailObj = soFarHighestAvailLookUp[constInfo["entity_tag"]]
        newHighestAvail = maxAvail
        newHighestAvailTime = maxAvailDt.to_pydatetime()
        if newHighestAvail < prevHighestAvailObj["value"]:
            newHighestAvail = prevHighestAvailObj["value"]
            newHighestAvailTime = prevHighestAvailObj["ts"]
        newHighestShortagePerc = round(
            100*(newHighestReq-newHighestAvail)/newHighestAvail, 2)
        newHighestAvailTime = newHighestAvailTime
        newHighestReqTime = newHighestReqTime
        mRepo.insertSoFarHighest(
            constInfo['entity_tag'], "soFarHighestAvailability", startDt, newHighestAvail, newHighestAvailTime)
        mRepo.insertSoFarHighest(
            constInfo['entity_tag'], "soFarHighestRequirement", startDt, newHighestReq, newHighestReqTime)

        const_display_row: ISoFarHighestDataRow = {
            'entity': constInfo['display_name'],
            'peakReqMW': round(maxReq),
            'peakAvailMW': round(maxAvail),
            'shortage_X': maxShortagePerc,
            'highestReqMW': round(newHighestReq),
            'highestAvailMW': round(newHighestAvail),
            'shortage_Y': newHighestShortagePerc,
            'highestReqMWDateStr': 'Max on {0} at {1} hrs'.format(dt.datetime.strftime(newHighestReqTime, "%d.%m.%y"),
                                                                  dt.datetime.strftime(newHighestReqTime, "%H:%M")),
            'highestAvailMWDateStr': 'Max on {0} at {1} hrs'.format(dt.datetime.strftime(newHighestAvailTime, "%d.%m.%y"),
                                                                    dt.datetime.strftime(newHighestAvailTime, "%H:%M"))
        }
        dispRows.append(const_display_row)

    secData: ISection_1_3_b = {"so_far_hig_req_avail": dispRows}
    return secData
