from src.typeDefs.aggregateMonthlyDataRecord import IAggregateDataRecord
import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.utils.getPrevFinYrDt import getPrevFinYrDt
import pandas as pd
from src.config.appConfig import getConstituentsMappings
import numpy as np
from src.typeDefs.section_1_9.section_1_9 import ISection_1_9, IScheduleDrawalDetails


def fetchSection1_9Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_9:
    constituentsInfos = getConstituentsMappings()

    constConfig = {}
    for c in constituentsInfos:
        constConfig[c["entity_tag"]] = c["display_name"]

    dataRecords = pd.DataFrame()
    mRepo = MetricsDataRepo(appDbConnStr)
    # get schedule and drawal MUs values for this month
    allEntityScheduleMuVals = mRepo.getAllEntityMetricMonthlyData(
        'Schedule (MU)', startDt, endDt)
    allEntityDrawalMuVals = mRepo.getAllEntityMetricMonthlyData(
        'Drawl (MU)', startDt, endDt)

    allEntityScheduleMuDf = pd.DataFrame(allEntityScheduleMuVals)
    allEntityDrawalMuDf = pd.DataFrame(allEntityDrawalMuVals)
    allEntityScheduleMuDf = allEntityScheduleMuDf.rename(columns={
        'metric_value': 'Schedule (MU)'})
    allEntityDrawalMuDf = allEntityDrawalMuDf.rename(columns={
        'metric_value': 'Drawl (MU)'})
    tempList = allEntityDrawalMuDf['Drawl (MU)']
    allEntityScheduleMuDf['Drawl (MU)'] = tempList

    allEntityScheduleMuDf['difference'] = round(
                                        (allEntityScheduleMuDf['Drawl (MU)'] -
                                        allEntityScheduleMuDf['Schedule (MU)']), 2)
    # print(allEntityReqMuDf)
    dataRecords = allEntityScheduleMuDf

    newNames = []
    for rIter in range(dataRecords.shape[0]):
        row = dataRecords.iloc[rIter, :]
        if row['entity_tag'] in constConfig:
            newNames.append(constConfig[row['entity_tag']])
        else:
            newNames.append(np.nan)
    dataRecords['entity_tag'] = newNames

    scheduleDrawalList: ISection_1_9["schedule_drawal"] = []

    for i in dataRecords.index:
        scheduleDrawal: IScheduleDrawalDetails = {
            'entity': dataRecords['entity_tag'][i],
            'schedule': round(dataRecords['Schedule (MU)'][i], 2),
            'drawal': round(dataRecords['Drawl (MU)'][i], 2),
            'difference': round(dataRecords['difference'][i], 2)
        }
        scheduleDrawalList.append(scheduleDrawal)
    
    sectionData: ISection_1_9 = {
        "schedule_drawal": scheduleDrawalList
    }

    return sectionData
