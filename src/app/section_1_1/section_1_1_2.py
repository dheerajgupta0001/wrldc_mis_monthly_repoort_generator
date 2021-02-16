from src.typeDefs.section_1_1.section_1_1_2 import ISection_1_1_2
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_2Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_2:
    
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', startDt, endDt)
    
    wrPeakDemDf = pd.DataFrame(wrDemVals)
    wrPeakDemDf = wrPeakDemDf.pivot(
        index='time_stamp', columns='metric_name', values='data_value')
    wrPeakDemDf['PeakDemand'] = wrPeakDemDf['Demand(MW)'] 

    lastYrStartDt = addMonths(startDt, -12)
    lastYrEndDt = addMonths(endDt, -12)
    # last_yr_month_name = dt.datetime.strftime(lastYrStartDt, "%b %y")

    wrLastYrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', lastYrStartDt, lastYrEndDt)
    
    wrLastYrPeakDemDf = pd.DataFrame(wrLastYrDemVals)
    wrLastYrPeakDemDf = wrLastYrPeakDemDf.pivot(
        index='time_stamp', columns='metric_name', values='data_value')
    wrLastYrPeakDemDf['PeakDemand'] = wrLastYrPeakDemDf['Demand(MW)'] 

    wr_max_peak_dem = round(wrPeakDemDf['PeakDemand'].max())
    maxPeakDemDt = wrPeakDemDf['PeakDemand'].idxmax()
    wr_max_peak_dem_time_str = "{0} Hrs on {1}".format(dt.datetime.strftime(
        maxPeakDemDt, "%H:%M"), dt.datetime.strftime(maxPeakDemDt, "%d-%b-%y"))

    wr_max_peak_dem_last_yr = round(wrLastYrPeakDemDf['PeakDemand'].max())

    wr_max_peak_dem_perc_inc = 100 * \
        (wr_max_peak_dem - wr_max_peak_dem)/wr_max_peak_dem
    wr_max_peak_dem_perc_inc = round(wr_max_peak_dem_perc_inc, 2)

    wr_avg_peak_dem = round(wrPeakDemDf['PeakDemand'].mean())
    wr_avg_peak_dem_last_yr = round(wrLastYrPeakDemDf['UnresDem'].mean())
    wr_avg_peak_dem_perc_inc = round(100 *
                                      (wr_avg_peak_dem - wr_avg_peak_dem_last_yr)/wr_avg_peak_dem_last_yr, 2)
    secData: ISection_1_1_2 = {
        'wr_peak_dem_met': wr_max_peak_dem,
        'wr_peak_dem_time_str': wr_max_peak_dem_time_str,
        'wr_max_peak_dem_perc_inc': wr_max_peak_dem_perc_inc,
        'wr_last_year_peak_dem': wr_max_peak_dem_last_yr,
        'wr_avg_peak_dem': wr_avg_peak_dem,
        'wr_avg_peak_dem_last_yr': wr_avg_peak_dem_last_yr,
        'wr_avg_peak_dem_perc_inc': wr_avg_peak_dem_perc_inc
    }
    return secData
