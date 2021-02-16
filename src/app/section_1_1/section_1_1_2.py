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

    lastYrStartDt = addMonths(startDt, -12)
    lastYrEndDt = addMonths(endDt, -12)
    # last_yr_month_name = dt.datetime.strftime(lastYrStartDt, "%b %y")

    wrLastYrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', lastYrStartDt, lastYrEndDt)

    wrLastYrPeakDemDf = pd.DataFrame(wrLastYrDemVals)
    wrLastYrPeakDemDf = wrLastYrPeakDemDf.pivot(
        index='time_stamp', columns='metric_name', values='data_value')

    wr_peak_dem = round(wrPeakDemDf['Demand(MW)'].max())
    maxPeakDemDt = wrPeakDemDf['Demand(MW)'].idxmax()
    wr_peak_dem_time_str = "{0} Hrs on {1}".format(dt.datetime.strftime(
        maxPeakDemDt, "%H:%M"), dt.datetime.strftime(maxPeakDemDt, "%d-%b-%y"))

    wr_peak_dem_last_yr = round(wrLastYrPeakDemDf['Demand(MW)'].max())

    wr_peak_dem_perc_inc = 100 * \
        (wr_peak_dem - wr_peak_dem_last_yr)/wr_peak_dem_last_yr
    wr_peak_dem_perc_inc = round(wr_peak_dem_perc_inc, 2)

    wr_avg_dem = round(wrPeakDemDf['Demand(MW)'].mean())
    wr_avg_dem_last_yr = round(wrLastYrPeakDemDf['Demand(MW)'].mean())
    wr_avg_dem_perc_inc = round(100 *
                                     (wr_avg_dem - wr_avg_dem_last_yr)/wr_avg_dem_last_yr, 2)
    secData: ISection_1_1_2 = {
        'wr_peak_dem_met': wr_peak_dem,
        'wr_peak_dem_time_str': wr_peak_dem_time_str,
        'wr_peak_dem_perc_inc': wr_peak_dem_perc_inc,
        'wr_last_year_peak_dem': wr_peak_dem_last_yr,
        'wr_avg_dem': wr_avg_dem,
        'wr_avg_dem_last_yr': wr_avg_dem_last_yr,
        'wr_avg_dem_perc_inc': wr_avg_dem_perc_inc
    }
    return secData
