from src.typeDefs.section_1_5.section_1_5_3 import ISection_1_5_3
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.utils.convertDtToDayNum import convertDtToDayNum
import matplotlib.pyplot as plt
import math


def fetchSection1_5_3Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_5_3:
    monthName = dt.datetime.strftime(startDt, "%b %y")
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR consumption Daily values for this month and prev yr month
    wrConVals = mRepo.getEntityMetricDailyData(
        'wr', 'Consumption(MU)', startDt, endDt)
    conVals = [x['data_value'] for x in wrConVals]
    wr_max_con = max(conVals)
    wrMaxConDt = wrConVals[conVals.index(wr_max_con)]['time_stamp']
    wr_max_con_date_str = dt.datetime.strftime(wrMaxConDt, "%d-%b-%y")
    wr_avg_con = sum(conVals)/len(conVals)
    # wrMaxDemTimestampStr = dt.datetime.strftime(
    #     wrMaxConDt, "%d-%b-%y %H:%M")+" hrs"

    lastYrStartDt = addMonths(startDt, -12)
    lastYrEndDt = addMonths(endDt, -12)
    monthNameLastYear = dt.datetime.strftime(lastYrStartDt, "%b %y")
    wrLastYrConVals = mRepo.getEntityMetricDailyData(
        'wr', 'Consumption(MU)', lastYrStartDt, lastYrEndDt)
    conVals = [x['data_value'] for x in wrLastYrConVals]
    wr_max_con_last_year = max(conVals)
    wr_max_con_date_str_last_year = dt.datetime.strftime(
        wrLastYrConVals[conVals.index(wr_max_con_last_year)]['time_stamp'], "%d-%b-%y")
    wr_avg_con_last_year = sum(conVals)/len(conVals)

    wr_avg_con_perc_change_last_year = round(
        100*(wr_avg_con-wr_avg_con_last_year)/wr_avg_con_last_year, 2)
    wr_max_con_perc_change_last_year = round(
        100*(wr_max_con-wr_max_con_last_year)/wr_max_con_last_year, 2)

    prevMonthStartDt = addMonths(startDt, -1)
    prevMonthEndDt = addMonths(endDt, -1)
    prev_month_name = dt.datetime.strftime(prevMonthStartDt, "%b %y")
    wrPrevMonthDemVals = mRepo.getEntityMetricDailyData(
        'wr', 'Consumption(MU)', prevMonthStartDt, prevMonthEndDt)
    conVals = [x['data_value'] for x in wrPrevMonthDemVals]
    wr_max_con_prev_month = max(conVals)
    wr_max_con_date_str_prev_month = dt.datetime.strftime(
        wrPrevMonthDemVals[conVals.index(wr_max_con_prev_month)]['time_stamp'], "%d-%b-%y")
    wr_avg_con_prev_month = sum(conVals)/len(conVals)

    wr_avg_con_perc_change_prev_month = round(
        100*(wr_avg_con-wr_avg_con_prev_month)/wr_avg_con_prev_month, 2)
    wr_max_con_perc_change_prev_month = round(
        100*(wr_max_con-wr_max_con_prev_month)/wr_max_con_prev_month, 2)

    # create plot image for demands of prev yr, prev month, this month
    pltDemObjs = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': monthName, 'val': x["data_value"]} for x in wrConVals]
    pltDemObjsLastYear = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': monthNameLastYear, 'val': x["data_value"]} for x in wrLastYrConVals]
    pltDemObjsPrevMonth = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': prev_month_name, 'val': x["data_value"]} for x in wrPrevMonthDemVals]
    pltDataObjs = pltDemObjs + pltDemObjsLastYear + pltDemObjsPrevMonth

    pltDataDf = pd.DataFrame(pltDataObjs)
    pltDataDf = pltDataDf.pivot(
        index='Date', columns='colName', values='val')
    pltDataDf.reset_index(inplace=True)
    pltDataDf["Date"] = [math.floor(x) for x in pltDataDf["Date"]]
    # pltDataDf = pltDataDf.groupby(by="Date").max()
    # save plot data as excel
    pltDataDf.to_excel("assets/plot_1_5_3.xlsx", index=True)
    
    # derive plot title
    pltTitle = 'Energy Cons-{0}, {1} & {2} \n Max- {3}MUs, {4}MUs and {5}MUs'.format(
        monthName, prev_month_name, monthNameLastYear, round(wr_max_con), round(wr_max_con_prev_month), round(wr_max_con_last_year))

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # set plot title
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('Date')
    ax.set_ylabel('MUs')
    # plot data and get the line artist object in return
    laThisMonth, = ax.plot(
        pltDataDf.index.values, pltDataDf[monthName].values, color='#ff0000')
    laThisMonth.set_label(monthName)

    laLastYear, = ax.plot(
        pltDataDf.index.values, pltDataDf[monthNameLastYear].values, color='#00ff00')
    laLastYear.set_label(monthNameLastYear)

    laPrevMonth, = ax.plot(
        pltDataDf.index.values, pltDataDf[prev_month_name].values, color='#A52A2A')
    laPrevMonth.set_label(prev_month_name)

    # enable y axis grid lines
    ax.yaxis.grid(True)
    ax.set_xlim((1, 31), auto=True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
              ncol=3, mode="expand", borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_1_5_3.png')

    secData: ISection_1_5_3 = {
        'prev_month_name': prev_month_name,
        'wr_max_con': round(wr_max_con),
        'wr_max_con_date_str': wr_max_con_date_str,
        'wr_avg_con': round(wr_avg_con),
        'wr_max_con_last_year': round(wr_max_con_last_year),
        'wr_max_con_date_str_last_year': wr_max_con_date_str_last_year,
        'wr_avg_con_last_year': round(wr_avg_con_last_year),
        'wr_avg_con_perc_change_last_year': wr_avg_con_perc_change_last_year,
        'wr_max_con_perc_change_last_year': wr_max_con_perc_change_last_year,
        'wr_max_con_prev_month': round(wr_max_con_prev_month),
        'wr_max_con_date_str_prev_month': wr_max_con_date_str_prev_month,
        'wr_avg_con_prev_month': round(wr_avg_con_prev_month),
        'wr_avg_con_perc_change_prev_month': wr_avg_con_perc_change_prev_month,
        'wr_max_con_perc_change_prev_month': wr_max_con_perc_change_prev_month
    }
    return secData
