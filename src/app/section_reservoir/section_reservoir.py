import datetime as dt
from typing import List, Any
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.utils.getPrevFinYrDt import getPrevFinYrDt
import pandas as pd
from src.config.appConfig import getReservoirsMappings
from src.utils.convertDtToDayNumMonth import convertDtToDayNumMonthYear
import math
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.dates as mdates
from src.typeDefs.reservoir_section.reservoir_section import IReservoirSection


def fetchReservoirContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> IReservoirSection:
    reservoirInfo = getReservoirsMappings()

    numPages = 0
    mRepo = MetricsDataRepo(appDbConnStr)
    prevFinYrStartDt = getPrevFinYrDt(startDt)
    prevFinYear = dt.datetime.strftime(prevFinYrStartDt, "%Y")
    currYear = int(prevFinYear) + 1

    # last financial year details
    lastFinYrStartDt = getPrevFinYrDt(prevFinYrStartDt)
    latsFinYrEndDt = prevFinYrStartDt - dt.timedelta(days=1)
    lastFinYrStarStr = dt.datetime.strftime(lastFinYrStartDt, "%Y")
    lastFinYrEndDt = int(lastFinYrStarStr) + 1

    for itr in reservoirInfo:
        metricList: List = []
        for entity in itr:
            if entity == 'entity_tag':
                continue
            else:
                metricList.append(mRepo.getReservoirDailyData(
                    itr['entity_tag'], itr[entity], prevFinYrStartDt, endDt))
        if len(metricList[0]) > 0:
            # create plot image for all the metrices
            pltDataObj: List = []
            for temp in range(len(metricList)):
                pltDataObj = pltDataObj + [{'Date':
                                            x["time_stamp"], 'colName': x["metric_tag"], 'val': x["data_value"]} for x in metricList[temp]]
            pltDataDf = pd.DataFrame(pltDataObj)
            pltDataDf = pltDataDf.pivot(
                index='Date', columns='colName', values='val')
            pltDataDf.reset_index(inplace=True)

            # derive plot title
            pltTitle = '{0} {1}-{2}'.format(itr['entity_tag'],
                                            prevFinYear, currYear)

            # create a plotting area and get the figure, axes handle in return
            fig, ax = plt.subplots(figsize=(7.5, 4.5))

            # instantiate a second axes that shares the same x-axis
            ax2 = ax.twinx()
            # set plot title
            ax.set_title(pltTitle)
            # set y labels
            ax2.set_ylabel('MUs')
            ax.set_ylabel('Meter')

            # set x axis locator as month
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            # set x axis formatter as month name
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

            # set x axis locator as month
            ax2.xaxis.set_major_locator(mdates.MonthLocator())
            # set x axis formatter as month name
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

            # plot data and get the line artist object in return 'GEN.'

            clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff']
            for col in range(len(pltDataDf.columns)-1):
                if pltDataDf.columns[col+1] == 'GEN.':
                    last, = ax2.plot(
                        pltDataDf['Date'], pltDataDf[pltDataDf.columns[col+1]
                                                     ], color=clr[col], label=pltDataDf.columns[col+1]
                    )
                else:
                    last, = ax.plot(
                        pltDataDf['Date'], pltDataDf[pltDataDf.columns[col+1]], color=clr[col], label=pltDataDf.columns[col+1])
            # enable y axis grid lines
            ax.yaxis.grid(True)

            # Ensure a major tick for each week using (interval=1)
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

            # enable legends
            ax2.legend()
            ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
                      ncol=3, mode="expand", borderaxespad=0.)
            fig.subplots_adjust(bottom=0.25, top=0.8)
            fig.savefig('assets/reservoir_section_{0}.png'.format(numPages))
            # fig.savefig('assets/reservoir_section/{0}-{1}.png'.format(itr['entity_tag'], currYear))
            plt.close()
            numPages += 1

        prevFinYrMetricList: List = []
        for entity in itr:
            if entity == 'entity_tag':
                continue
            else:
                prevFinYrMetricList.append(mRepo.getReservoirDailyData(
                    itr['entity_tag'], itr[entity], lastFinYrStartDt, latsFinYrEndDt))
        if len(prevFinYrMetricList[0]) > 0:
            # create plot image for all the metrices
            lastFinYrPltDataObj: List = []
            for temp in range(len(prevFinYrMetricList)):
                lastFinYrPltDataObj = lastFinYrPltDataObj + [{'Date': x["time_stamp"],
                                        'colName': x["metric_tag"], 'val': x["data_value"]} for x in prevFinYrMetricList[temp]]
            lastFinYrPltDataDf = pd.DataFrame(lastFinYrPltDataObj)
            lastFinYrPltDataDf = lastFinYrPltDataDf.pivot(
                index='Date', columns='colName', values='val')
            lastFinYrPltDataDf.reset_index(inplace=True)

            # derive plot title
            pltTitle = '{0} {1}-{2}'.format(itr['entity_tag'],
                                            lastFinYrStarStr, lastFinYrEndDt)

            # create a plotting area and get the figure, axes handle in return
            fig, ax = plt.subplots(figsize=(7.5, 4.5))

            # instantiate a second axes that shares the same x-axis
            ax2 = ax.twinx()
            # set plot title
            ax.set_title(pltTitle)
            # set y labels
            ax2.set_ylabel('MUs')
            ax.set_ylabel('Meter')

            # set x axis locator as month
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            # set x axis formatter as month name
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

            # set x axis locator as month
            ax2.xaxis.set_major_locator(mdates.MonthLocator())
            # set x axis formatter as month name
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            
            # plot data and get the line artist object in return 'GEN.'

            clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff']
            for col in range(len(lastFinYrPltDataDf.columns)-1):
                if lastFinYrPltDataDf.columns[col+1] == 'GEN.':
                    last, = ax2.plot(
                        lastFinYrPltDataDf['Date'], lastFinYrPltDataDf[lastFinYrPltDataDf.columns[col+1]],
                                                    color=clr[col], label=lastFinYrPltDataDf.columns[col+1]
                    )
                else:
                    last, = ax.plot(
                        lastFinYrPltDataDf['Date'], lastFinYrPltDataDf[lastFinYrPltDataDf.columns[col+1]],
                                                    color=clr[col], label=lastFinYrPltDataDf.columns[col+1])
            # enable y axis grid lines
            ax.yaxis.grid(True)
            # Ensure a major tick for each week using (interval=1)
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

            # enable legends
            ax2.legend()
            ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
                      ncol=3, mode="expand", borderaxespad=0.)
            fig.subplots_adjust(bottom=0.25, top=0.8)
            fig.savefig('assets/reservoir_section_{0}.png'.format(numPages))

            # fig.savefig('assets/reservoir_section/{0}-{1}.png'.format(itr['entity_tag'],
            #                                         lastFinYrEndDt))
            plt.close()
            numPages += 1

    sectionData: IReservoirSection = {'num_plts_sec_reservoir': numPages}
    return sectionData