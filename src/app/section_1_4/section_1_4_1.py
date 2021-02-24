from typing import List
from src.typeDefs.section_1_4.section_1_4_1 import ISection_1_4_1, IDemDataRow_1_4_1
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.config.appConfig import getConstituentsMappings
from src.typeDefs.config.appConfig import IConstituentConfig


def fetchSection1_4_1Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_4_1:
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR demand hourly values for this month and prev yr month
    # Load Shedding(MW)

    # initialize demand rows
    dem_data_1_4_1: List[IDemDataRow_1_4_1] = []

    constList: List[IConstituentConfig] = getConstituentsMappings()

    for con in constList:
        cTag = con["entity_tag"]
        cName = con["display_name"]
        cDemVals = mRepo.getEntityMetricHourlyData(
            cTag, 'Demand(MW)', startDt, endDt)
        cLsVals = mRepo.getEntityMetricHourlyData(
            'wr', 'Load Shedding(MW)', startDt, endDt)
        cDemDf = pd.DataFrame(cDemVals+cLsVals)
        cDemDf = cDemDf.pivot(
            index="time_stamp", columns="metric_name", values="data_value")
        cDemDf["Req"] = cDemDf["Demand(MW)"] + cDemDf["Load Shedding(MW)"]
        # get max month demand met
        maxDem = cDemDf["Demand(MW)"].max()
        maxDemDt = cDemDf["Demand(MW)"].idxmax().to_pydatetime()
        maxDemDateStr = dt.datetime.strftime(maxDemDt, "%d-%m-%Y")
        maxDemTimeStr = dt.datetime.strftime(maxDemDt, "%H:%M")
        freqSamples = mRepo.getRawFreq(maxDemDt, maxDemDt)
        freqAtMaxDem = 50
        if len(freqSamples) > 0:
            freqAtMaxDem = freqSamples[0]["frequency"]
        maxReq = cDemDf["Req"].max()
        maxReqDt = cDemDf["Req"].idxmax()
        lsAtMaxReq = cDemDf["Load Shedding(MW)"].loc[maxReqDt]
        maxReqDateStr = dt.datetime.strftime(
            maxReqDt.to_pydatetime(), "%d-%m-%Y")
        maxReqTimeStr = dt.datetime.strftime(maxReqDt.to_pydatetime(), "%H:%M")
        freqSamples = mRepo.getRawFreq(maxDemDt, maxDemDt)
        freqAtMaxReq = 50
        if len(freqSamples) > 0:
            freqAtMaxReq = freqSamples[0]["frequency"]
        freqCorrAtMaxReq = 0
        # TODO find freq correction at max req
        if freqAtMaxReq < 50:
            freqCorrAtMaxReq = 0.035*demMetAtMaxReq*(50-freqAtMaxReq)
        reqPlusFreqCorrAtMaxReq = maxReq + freqCorrAtMaxReq
        demMetAtMaxReq = maxReq - lsAtMaxReq
        dem_data_1_4_1.extend([
            {
                'state_name': cName,
                'catered': "",
                'ls': "",
                'freq_corr': "",
                'pc': "",
                'tot_dem': "",
                'peak_date': "",
                'peak_time': "",
                'freq_at_peak': ""
            },
            {
                'state_name': "Registered",
                'catered': round(maxDem),
                'ls': "",
                'freq_corr': "",
                'pc': "",
                'tot_dem': round(maxDem),
                'peak_date': maxDemDateStr,
                'peak_time': maxDemTimeStr,
                'freq_at_peak': round(freqAtMaxDem, 3)
            },
            {
                'state_name': "Un-Restricted",
                'catered': round(demMetAtMaxReq),
                'ls': round(lsAtMaxReq, 1),
                'freq_corr': round(freqCorrAtMaxReq, 1),
                'pc': "0",
                'tot_dem': round(reqPlusFreqCorrAtMaxReq),
                'peak_date': maxReqDateStr,
                'peak_time': maxReqTimeStr,
                'freq_at_peak': round(freqAtMaxReq, 3)
            }
        ])
    secData: ISection_1_4_1 = {
        'dem_data_1_4_1': dem_data_1_4_1
    }
    return secData
