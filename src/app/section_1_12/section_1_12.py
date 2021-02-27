from src.typeDefs.section_1_1.section_1_1_3 import ISection_1_1_3
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
import math
import matplotlib.pyplot as plt
from src.utils.convertDtToDayNum import convertDtToDayNum


def fetchSection1_12Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_3:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    month_name = dt.datetime.strftime(startDt, "%b %y")
    mRepo = MetricsDataRepo(appDbConnStr)
    width = 0.3
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrErActMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'EAST REGION_NET ACT (MU)', startDt, endDt)

    wrErSchMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'EAST REGION_NET SCH(MU)', startDt, endDt)

    # create plot image for demands of prev yr, prev month, this month
    pltWrErActObjs = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrErActMuVals]
    pltWrErSchObjs = [{'Date': convertDtToDayNum(
        x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrErSchMuVals]
    pltDataObjs = pltWrErActObjs + pltWrErSchObjs

    pltDataDf = pd.DataFrame(pltDataObjs)
    pltDataDf = pltDataDf.pivot(
        index='Date', columns='colName', values='val')
    pltDataDf.reset_index(inplace=True)
    pltDataDf["Date"] = [math.floor(x) for x in pltDataDf["Date"]]

    # derive plot title
    pltTitle = 'WR - ER EXCHANGES FOR {0}'.format(month_name)

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # set plot title
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('Date')
    ax.set_ylabel('MW')
    # plot data and get the line artist object in return
    plt.bar(pltDataDf['Date']- width, pltDataDf['EAST REGION_NET ACT (MU)'], width= width, color='#bf4040', label='ACTUAL')

    plt.bar(pltDataDf['Date'], pltDataDf['EAST REGION_NET SCH(MU)'], width= width, color='#4d88ff', label='SCH')
    
    # ax.set_xlim((1, 31), auto=True)
    # enable y axis grid lines
    ax.yaxis.grid(True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
              ncol=3, mode="expand", borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    plt.show()
    fig.savefig('assets/section_1_12_1.png')

    # section 1_12_2
    
    return True
