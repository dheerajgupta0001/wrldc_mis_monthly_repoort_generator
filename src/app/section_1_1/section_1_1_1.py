from src.typeDefs.section_1_1.section_1_1_1 import ISection_1_1_1
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_1Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_1:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    month_name = dt.datetime.strftime(startDt, "%b' %y")
    full_month_name = dt.datetime.strftime(startDt, "%B %Y")
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', startDt, endDt)
    wrLoadSheddingVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Load Shedding(MW)', startDt, endDt)
    wrUnResDemDf = pd.DataFrame(wrDemVals+wrLoadSheddingVals)
    wrUnResDemDf = wrUnResDemDf.pivot(
        index='time_stamp', columns='metric_name', values='data_value')
    wrUnResDemDf['UnresDem'] = wrUnResDemDf['Demand(MW)'] + \
        wrUnResDemDf['Load Shedding(MW)']

    lastYrStartDt = addMonths(startDt, -12)
    lastYrEndDt = addMonths(endDt, -12)
    last_yr_month_name = dt.datetime.strftime(lastYrStartDt, "%b %y")
    wrLastYrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', lastYrStartDt, lastYrEndDt)
    wrLastYrLoadSheddingVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Load Shedding(MW)', lastYrStartDt, lastYrStartDt)
    wrLastYrUnResDemDf = pd.DataFrame(wrLastYrDemVals+wrLastYrLoadSheddingVals)
    wrLastYrUnResDemDf = wrLastYrUnResDemDf.pivot(
        index='time_stamp', columns='metric_name', values='data_value')
    wrLastYrUnResDemDf['UnresDem'] = wrLastYrUnResDemDf['Demand(MW)'] + \
        wrLastYrUnResDemDf['Load Shedding(MW)']

    wr_max_unres_dem = round(wrUnResDemDf['UnresDem'].max())
    maxUnresDemDt = wrUnResDemDf['UnresDem'].idxmax()
    wr_max_unres_dem_time_str = "{0} Hrs on {1}".format(dt.datetime.strftime(
        maxUnresDemDt, "%H:%M"), dt.datetime.strftime(maxUnresDemDt, "%d-%b-%y"))

    wr_max_unres_dem_last_yr = round(wrLastYrUnResDemDf['UnresDem'].max())

    wr_max_unres_dem_perc_inc = 100 * \
        (wr_max_unres_dem - wr_max_unres_dem_last_yr)/wr_max_unres_dem_last_yr
    wr_max_unres_dem_perc_inc = round(wr_max_unres_dem_perc_inc, 2)

    wr_avg_unres_dem = round(wrUnResDemDf['UnresDem'].mean())
    wr_avg_unres_dem_last_yr = round(wrLastYrUnResDemDf['UnresDem'].mean())
    wr_avg_unres_dem_perc_inc = round(100 *
                                      (wr_avg_unres_dem - wr_avg_unres_dem_last_yr)/wr_avg_unres_dem_last_yr, 2)
    secData: ISection_1_1_1 = {
        'monthDtObj': monthDtObj,
        'month_name': month_name,
        'full_month_name': full_month_name,
        'last_yr_month_name': last_yr_month_name,
        'wr_max_unres_dem': wr_max_unres_dem,
        'wr_max_unres_dem_time_str': wr_max_unres_dem_time_str,
        'wr_max_unres_dem_perc_inc': wr_max_unres_dem_perc_inc,
        'wr_max_unres_dem_last_yr': wr_max_unres_dem_last_yr,
        'wr_avg_unres_dem': wr_avg_unres_dem,
        'wr_avg_unres_dem_last_yr': wr_avg_unres_dem_last_yr,
        'wr_avg_unres_dem_perc_inc': wr_avg_unres_dem_perc_inc
    }
    return secData
