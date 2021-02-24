from src.typeDefs.section_1_7.section_1_7_2 import ISection_1_7_2
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd


def fetchSection1_7_2Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_7_2:
    mRepo = MetricsDataRepo(appDbConnStr)

    # get voltage data for this month
    maxVoltData = mRepo.getDailyVoltDataByLevel(400, "Max", startDt, endDt)
    maxVoltDf = pd.DataFrame(maxVoltData)
    maxVoltDf["data_val"] = pd.to_numeric(
        maxVoltDf["data_val"], errors='coerce')
    maxVoltSeries = maxVoltDf.groupby("entity_name").apply(getMax)
    maxVoltSeries = maxVoltSeries.round()
    maxVoltSeries = maxVoltSeries.rename("max_vol")

    minVoltData = mRepo.getDailyVoltDataByLevel(400, "Min", startDt, endDt)
    minVoltDf = pd.DataFrame(minVoltData)
    minVoltDf["data_val"] = pd.to_numeric(
        minVoltDf["data_val"], errors='coerce')
    minVoltSeries = minVoltDf.groupby("entity_name").apply(getMin)
    minVoltSeries = minVoltSeries.round()
    minVoltSeries = minVoltSeries.rename("min_vol")

    lessVoltPercData = mRepo.getDailyVoltDataByLevel(
        400, "%Time <380 or 728", startDt, endDt)
    lessVoltPercDf = pd.DataFrame(lessVoltPercData)
    lessVoltPercDf["data_val"] = pd.to_numeric(
        lessVoltPercDf["data_val"], errors='coerce')
    lessVoltPercSeries = lessVoltPercDf.groupby("entity_name").apply(getMean)
    lessVoltPercSeries = lessVoltPercSeries.round(2)
    lessVoltPercSeries = lessVoltPercSeries.rename("less_perc")

    bandVoltPercData = mRepo.getDailyVoltDataByLevel(
        400, "%Time within IEGC Band", startDt, endDt)
    bandVoltPercDf = pd.DataFrame(bandVoltPercData)
    bandVoltPercDf["data_val"] = pd.to_numeric(
        bandVoltPercDf["data_val"], errors='coerce')
    bandVoltPercSeries = bandVoltPercDf.groupby("entity_name").apply(getMean)
    bandVoltPercSeries = bandVoltPercSeries.round(2)
    bandVoltPercSeries = bandVoltPercSeries.rename("band_perc")

    moreVoltPercData = mRepo.getDailyVoltDataByLevel(
        400, "%Time >420 or 800", startDt, endDt)
    moreVoltPercDf = pd.DataFrame(moreVoltPercData)
    moreVoltPercDf["data_val"] = pd.to_numeric(
        moreVoltPercDf["data_val"], errors='coerce')
    moreVoltPercSeries = moreVoltPercDf.groupby("entity_name").apply(getMean)
    moreVoltPercSeries = moreVoltPercSeries.round(2)
    moreVoltPercSeries = moreVoltPercSeries.rename("more_perc")

    numMonthHrs = (endDt - startDt).total_seconds()/(60*60)

    secDf = pd.concat([maxVoltSeries, minVoltSeries, lessVoltPercSeries,
                       bandVoltPercSeries, moreVoltPercSeries], axis=1)
    secDf['less_hrs'] = secDf['less_perc']*(numMonthHrs*0.01)
    secDf['more_hrs'] = secDf['more_perc']*(numMonthHrs*0.01)
    secDf['out_hrs'] = secDf['less_hrs'] + secDf['more_hrs']
    secDf['vdi'] = secDf['out_hrs']*(1/numMonthHrs)
    secDf['less_hrs'] = secDf['less_hrs'].apply(hrsToDurationStr)
    secDf['more_hrs'] = secDf['more_hrs'].apply(hrsToDurationStr)
    secDf['out_hrs'] = secDf['out_hrs'].apply(hrsToDurationStr)
    secDf['vdi'] = secDf['vdi'].apply(hrsToDurationStr)
    secDf.reset_index(inplace=True)
    secDf['entity_name'] = secDf['entity_name'].apply(strip400)
    secDf.rename(columns={"entity_name": "station"}, inplace=True)
    secDataRows = secDf.to_dict('records')

    sectionData: ISection_1_7_2 = {
        'voltVdiProfile400': secDataRows
    }

    return sectionData


def getMax(x):
    vals = [p for p in x['data_val'] if not pd.isna(p)]
    maxVal = max(vals)
    return maxVal


def getMin(x):
    vals = [p for p in x['data_val'] if (not pd.isna(p) and (p > 1))]
    minVal = min(vals)
    return minVal


def getMean(x):
    vals = [p for p in x['data_val'] if not pd.isna(p)]
    percVal = sum(vals)/len(vals)
    return percVal


def hrsToDurationStr(hrs):
    durStr = "{0}:{1}".format(int(hrs), int((hrs % 1)*60))
    return durStr


def strip400(nStr: str):
    return nStr.replace(' - 400KV', '')
