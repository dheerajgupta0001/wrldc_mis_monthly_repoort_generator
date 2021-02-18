from src.typeDefs.aggregateMonthlyDataRecord import IAggregateDataRecord
import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.config.appConfig import getConstituentsMappings
import numpy as np
from src.typeDefs.section_1_3.section_1_3_b import ISection_1_3_b


def fetchSection1_3_bContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[ISection_1_3_b]:
    constituentsInfos = getConstituentsMappings()
    metricNamesdb = {
        'loadShedding':'Load Shedding(MW)',
        'peakAvailability':'Demand(MW)',
        'peakRequirement': 'loadShedding + peakAvailability',
        'soFarHighestRequirement': 'Requirement (MW) ', 
        'soFarHighestAvailability' : 'Availability (MW) '
    }
    metricValueRename = {
        'peakRequirement':'Peak Requirement (MW) ' ,
        'peakAvailability':'Peak Availability (MW)' , 
        'soFarHighestRequirement': 'So Far Highest Requirement (MW) ',
        'soFarHighestAvailability' : 'So Far Highest Availability (MW) ',
        'so_far_highest_req_time':'So Far Highest Requirement Date and Time',
        'so_far_highest_avail_time':'So Far Highest Requirement Date and Time'
    }
    constConfig = {}
    for c in constituentsInfos:
        constConfig[c["entity_tag"]] = c["display_name"]

    dataRecords = pd.DataFrame()
    mRepo = MetricsDataRepo(appDbConnStr)

    allEntityPeakloadSheddingMWVals = mRepo.getAllEntityMetricHourlyData(
        metricNamesdb['loadShedding'] , startDt ,endDt
    )
    allEntityPeakAvailMWVals = mRepo.getAllEntityMetricHourlyData(
        metricNamesdb['peakAvailability'], startDt, endDt)

    allEntityPeakloadSheddingMWDf = pd.DataFrame(allEntityPeakloadSheddingMWVals)
    allEntityPeakAvailMWDf = pd.DataFrame(allEntityPeakAvailMWVals)

    allEntityPeakReqMWDf = allEntityPeakAvailMWDf
    allEntityPeakReqMWDf['data_value'] = allEntityPeakAvailMWDf['data_value'] + allEntityPeakloadSheddingMWDf['data_value']
# check if upper stmt works or not
    allEntityPeakAvailMWDf = allEntityPeakAvailMWDf.rename(columns={
        'data_value':metricValueRename['peakAvailability'],'time_stamp':'time_stamp_req'})
    allEntityPeakReqMWDf = allEntityPeakReqMWDf.rename(columns={
        'data_value': metricValueRename['peakRequirement'],'time_stamp':'time_stamp_avail'})

    tempList = allEntityPeakAvailMWDf[metricValueRename['peakAvailability']]
    allEntityPeakReqMWDf[metricValueRename['peakAvailability']] = tempList

    allEntityPeakReqMWDf['shortage_X'] = round(100 *
                                         (allEntityPeakReqMWDf[metricValueRename['peakRequirement']] -
                                          allEntityPeakReqMWDf[metricValueRename['peakAvailability']]) /
                                         allEntityPeakReqMWDf[metricValueRename['peakAvailability']], 2)
    # targetMonth should be 1 month before current month
    targetMonth = addMonths(startDt, -1)
    soFarHighestAllEntityReqMWVals = mRepo.getSoFarHighestAllEntityData(
        metricNamesdb['soFarHighestRequirement'],targetMonth)

    soFarHighestAllEntityAvailMWVals = mRepo.getSoFarHighestAllEntityData(
        metricNamesdb['soFarHighestAvailability'], targetMonth)

    soFarHighestAllEntityReqMWDf = pd.DataFrame(soFarHighestAllEntityReqMWVals)
    soFarHighestAllEntityAvailMWDf = pd.DataFrame(soFarHighestAllEntityAvailMWVals)

    soFarHighestAllEntityAvailMWDf = soFarHighestAllEntityAvailMWDf.rename(columns={
        'data_value': metricValueRename['soFarHighestAvailability'],
        'data_time':metricValueRename['so_far_highest_req_time']})

    soFarHighestAllEntityReqMWDf = soFarHighestAllEntityReqMWDf.rename(columns={
        'data_value': metricValueRename['soFarHighestRequirement'] ,
        'data_time':metricValueRename['so_far_highest_avail_time']})

    tempList = soFarHighestAllEntityAvailMWDf[metricValueRename['soFarHighestAvailability']]
    soFarHighestAllEntityReqMWDf[metricValueRename['soFarHighestAvailability']] = tempList

    soFarHighestAllEntityReqMWDf['shortage_Y'] = round(100 *
                                               (soFarHighestAllEntityReqMWDf[metricValueRename['soFarHighestRequirement']] -
                                                soFarHighestAllEntityAvailMWDf[metricValueRename['soFarHighestAvailability']]) /
                                               soFarHighestAllEntityAvailMWDf[metricValueRename['soFarHighestAvailability']], 2)
    soFarHighestAllEntityReqMWDf.set_index('constituent')
    dataRecords = pd.merge(
        allEntityPeakReqMWDf, soFarHighestAllEntityReqMWDf, on='constituent')

    # This code below is for displaying names as per config sheet
    newNames = []
    for rIter in range(dataRecords.shape[0]):
        row = dataRecords.iloc[rIter, :]
        if row['constituent'] in constConfig:
            newNames.append(constConfig[row['constituent']])
        else:
            newNames.append(np.nan)
    dataRecords['constituents'] = newNames

    # Update the so far highest table if req ,avail > so far highest

    for rIter in range(dataRecords.shape[0]):
        row = dataRecords.iloc[rIter,:]

        constituent = row['constituent']
        
        monthPeakReq = row[metricValueRename['peakRequirement']]
        monthPeakAvail = row[metricValueRename['peakAvailability']]

        monthPeakReqTime = row['time_stamp_req']
        monthPeakAvailTime = row['time_stamp_avail']

        soFarHighestReq = row[metricValueRename['soFarHighestRequirement']]
        soFarHighestAvail = row[metricValueRename['soFarHighestAvailability']]

        if monthPeakReq > soFarHighestReq:
            row['shortage_Y'] = updateShortage_Y(row['shortage_Y'] ,soFarHighestReq, soFarHighestAvail)
            metricName = metricValueRename['peakRequirement']
            mRepo.updateSoFarHighestTable(constituent,metricName,targetMonth,monthPeakReq,monthPeakReqTime)

        if monthPeakAvail > soFarHighestAvail:
            row['shortage_Y'] = updateShortage_Y(row['shortage_Y'] ,soFarHighestReq, soFarHighestAvail)
            metricName = metricValueRename['peakAvailability']
            mRepo.updateSoFarHighestTable(constituent,metricName,targetMonth,monthPeakAvail,monthPeakAvailTime)
           
    power_req_so_far_hgst: List[ISection_1_3_b["power_req_and_avail_and_so_far_highest"]] = []

    for i in dataRecords.index:
        highestReqTime = dataRecords[metricValueRename['so_far_highest_req_time']][i]
        highestAvailTime = dataRecords[metricValueRename['so_far_highest_avail_time']][i]

        hgReqTimeStr = 'Max on {0} at {1} hrs'.format(dt.datetime.strftime(highestReqTime,"%d.%m.%y"),
        dt.datetime.strftime(highestReqTime,"%H:%M"))

        hgAvailTimeStr = 'Max on {0} at {1} hrs'.format(dt.datetime.strftime(highestAvailTime,"%d.%m.%y"),
        dt.datetime.strftime(highestAvailTime,"%H:%M"))

        powr_so_far_single: ISection_1_3_b = {
            'entity': dataRecords['constituent'][i],
            'peakReqMW': round(dataRecords[metricValueRename['peakRequirement']][i], 2),
            'peakAvailMW': round(dataRecords[metricValueRename['peakAvailability']][i], 2),
            'shortage_X': round(dataRecords['shortage_X'][i], 2),
            'highestReqMW': round(dataRecords[metricValueRename['soFarHighestRequirement']][i], 2),
            'highestAvailMW': round(dataRecords[metricValueRename['soFarHighestAvailability']][i], 2),
            'shortage_Y': round(dataRecords['shortage_Y'][i], 2),
            'highestReqMWDateStr':hgReqTimeStr,
            'highestAvailMWDateStr':hgAvailTimeStr
        }
        power_req_so_far_hgst.append(powr_so_far_single)
    
    return power_req_so_far_hgst

def updateShortage_Y(shortage_Y , req , avail):
    shortage_Y  = round(100 *(req - avail)/avail , 2)
    return shortage_Y
