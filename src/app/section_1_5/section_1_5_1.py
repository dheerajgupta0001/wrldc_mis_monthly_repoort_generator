import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.utils.convertDtToDayNum import convertDtToDayNum
from src.utils.getPrevFinYrDt import getPrevFinYrDt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fetchSection1_5_1Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:
    # TODO complete this
    # get WR demand from recent Fin year start till this month
    # and WR demand from 2 years back fin year to last fin year
    # example: For Jan 21, we require data from 1-Apr-2019 to 31-Mar-2020 and 1-Apr-2020 to 31 Jan 21

    finYrStart = getPrevFinYrDt(startDt)
    prevFinYrStart = getPrevFinYrDt(finYrStart)

    finYrName = '{0}-{1}'.format(finYrStart.year, (finYrStart.year+1) % 100)
    prevFinYrName = '{0}-{1}'.format(finYrStart.year-1, finYrStart.year % 100)
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR hourly demand values for this financial year
    wrDemVals = mRepo.getEntityMetricDailyData(
        'wr', 'Max Demand(MW)', finYrStart, endDt)
    wrPrevFinYrDemVals = mRepo.getEntityMetricDailyData(
        'wr', 'Max Demand(MW)', prevFinYrStart, finYrStart-dt.timedelta(days=1))

    # create plot image for demands of prev fin year and this fin year
    pltDemObjs = [{'MONTH': x["time_stamp"], 'colName': finYrName,
                   'val': x["data_value"]} for x in wrDemVals]
    pltDemObjsLastYear = [{'MONTH': x["time_stamp"],
                           'colName': prevFinYrName, 'val': x["data_value"]} for x in wrPrevFinYrDemVals]

    pltDataObjs = pltDemObjs + pltDemObjsLastYear

    pltDataDf = pd.DataFrame(pltDataObjs)
    pltDataDf = pltDataDf.pivot(
        index='MONTH', columns='colName', values='val')
    # save plot data as excel
    pltDataDf.to_excel("assets/plot_1_5_1.xlsx", index=True)

    # derive plot title
    pltTitle = 'WR seasonal demand (daily max.) Plot {0} to {1}'.format(
        prevFinYrName, finYrName)

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots()
    # set plot title
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('MONTH')
    ax.set_ylabel('MW')

    # set x axis locator as month
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    # set x axis formatter as month name
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # ax.set_xlim(xmin=finYrStart)

    # plot data and get the line artist object in return
    laThisYr, = ax.plot(
        pltDataDf.index.values, pltDataDf[finYrName].values, color='#0000ff')
    laThisYr.set_label(finYrName)

    laLastYear, = ax.plot(
        [addMonths(x, 12) for x in pd.Series(pltDataDf.index).dt.to_pydatetime()], pltDataDf[prevFinYrName].values, color='#ff0000')
    laLastYear.set_label(prevFinYrName)

    # enable axis grid lines
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
              ncol=2, borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_1_5_1.png')

    secData: dict = {}
    return secData
