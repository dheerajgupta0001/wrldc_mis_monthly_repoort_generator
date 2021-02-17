from src.typeDefs.section_1_1.section_1_1_4 import ISection_1_1_4
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_4Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_4:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    month_name = dt.datetime.strftime(startDt, "%b %y")
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrConMuVals = mRepo.getEntityMetricDailyData(
        'wr', 'Requirement (MU)', startDt, endDt)
    wrConMuDf = pd.DataFrame(wrConMuVals)
    wrConMuDf = wrConMuDf.pivot(
        index='time_stamp', columns='metric_name', values='data_value')

    lastYrStartDt = addMonths(startDt, -12)
    lastYrEndDt = addMonths(endDt, -12)
    last_yr_month_name = dt.datetime.strftime(lastYrStartDt, "%b %y")
    wrLastYrConMuVals = mRepo.getEntityMetricDailyData(
        'wr', 'Requirement (MU)', lastYrStartDt, lastYrEndDt)
    wrLastYrConMuDf = pd.DataFrame(wrLastYrConMuVals)
    wrLastYrConMuDf = wrLastYrConMuDf.pivot(
        index='time_stamp', columns='metric_name', values='data_value')

    wr_tot_req_mu = round(wrConMuDf['Requirement (MU)'].sum())
    wr_avg_req_mu = round(wrConMuDf['Requirement (MU)'].mean())
    wr_max_req_mu = round(wrConMuDf['Requirement (MU)'].max())
    wrMaxConsMuDate = wrConMuDf['Requirement (MU)'].idxmax()
    wr_avg_req_mu_last_yr = round(wrLastYrConMuDf['Requirement (MU)'].mean())

    wr_max_req_mu_date = "{0}".format(dt.datetime.strftime(wrMaxConsMuDate, "%d-%b-%y"))

    wr_avg_req_mu_perc_inc = round(100 *
                                      (wr_avg_req_mu - wr_avg_req_mu_last_yr)/wr_avg_req_mu_last_yr, 2)
    secData: ISection_1_1_4 = {
        'wr_tot_req_mu': wr_tot_req_mu,
        'wr_avg_req_mu': wr_avg_req_mu,
        'wr_max_req_mu': wr_max_req_mu,
        'wr_max_req_mu_date': wr_max_req_mu_date,
        'wr_avg_req_mu_perc_inc': wr_avg_req_mu_perc_inc,
        'wr_avg_req_mu_last_yr': wr_avg_req_mu_last_yr
    }
    return secData
