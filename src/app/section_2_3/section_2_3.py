from src.typeDefs.section_2_3.section_2_3 import ISection_2_3_1, ISection_2_3_2
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
import matplotlib.pyplot as plt
from src.config.appConfig import getConstituentsMappings
import matplotlib.dates as mdates
from src.utils.convertDtToDayNum import convertDtToDayNum


def fetchSection2_3_MaxContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_2_3_1:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    month_name = dt.datetime.strftime(startDt, "%b' %y")
    full_month_name = dt.datetime.strftime(startDt, "%B %Y")
    constituentinfo=getConstituentsMappings()
    numPages=0

    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', startDt, endDt)

    wrUnResDemDf = pd.DataFrame(wrDemVals)
    wrUnResDemDf = wrUnResDemDf.set_index('time_stamp')

    wr_max_unres_dem = round(wrUnResDemDf['data_value'].max())
    maxUnresDemDt = wrUnResDemDf['data_value'].idxmax()

    maxDtSrtT=dt.datetime(maxUnresDemDt.year,maxUnresDemDt.month,maxUnresDemDt.day)
    maxDtEndT=dt.datetime(maxUnresDemDt.year,maxUnresDemDt.month,maxUnresDemDt.day,23)
    wr_max_unres_dem_time_str = "HOURLY DEMAND CURVES ON REGIONAL PEAK DAY {1} at {0} Hrs".format(dt.datetime.strftime(
        maxUnresDemDt, "%H:%M"), dt.datetime.strftime(maxUnresDemDt, "%d-%b-%y"))
    wrUnResDemDf= wrUnResDemDf[ (wrUnResDemDf.index>=maxDtSrtT) & (wrUnResDemDf.index<=maxDtEndT)]

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    # set plot title
    pltTitle="WR"
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('HOUR')
    ax.set_ylabel('MW')
    ax.set_facecolor("violet")
    fig.patch.set_facecolor('#95d0fc')


    wrUnResDemDf.reset_index(inplace=True)
    dateList = []
    times = wrUnResDemDf["time_stamp"]
    for col in times:
            dateList.append(dt.datetime.strftime(col, '%H'))

    wrUnResDemDf["time_stamp"] = dateList
    # plot data and get the line artist object in return
    laThisMonth, = ax.plot(wrUnResDemDf['time_stamp'],
                        wrUnResDemDf['data_value'], color='#0000ff')


    # enable axis grid lines
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.suptitle(wr_max_unres_dem_time_str, fontsize=10)

    # plt.show()
    fig.savefig('assets/section_2_3_1_{0}.png'.format(numPages))
    numPages+= 1

    for itr in constituentinfo:
        if itr['entity_tag']=='wr':
            continue
        else:

            # get WR Unrestricted demand hourly values for this month and prev yr month
            constDemVals = mRepo.getEntityMetricHourlyData(
                itr['entity_tag'], 'Demand(MW)', maxDtSrtT, maxDtEndT)

            constUnResDemDf = pd.DataFrame(constDemVals)
            constUnResDemDf = constUnResDemDf.set_index('time_stamp')
            constUnResDemDf.reset_index(inplace=True)
            dateList = []
            times = constUnResDemDf["time_stamp"]
            for col in times:
                dateList.append(dt.datetime.strftime(col, '%H'))

            constUnResDemDf["time_stamp"] = dateList

            # create a plotting area and get the figure, axes handle in return
            fig, ax = plt.subplots(figsize=(7.5, 2.5))
            # set plot title
            pltTitle = itr['display_name']
            ax.set_title(pltTitle)
            # set x and y labels
            ax.set_xlabel('HOUR')
            ax.set_ylabel('MW')
            laThisMonth, = ax.plot(constUnResDemDf['time_stamp'],
                                   constUnResDemDf['data_value'], color='#0000ff')
            # enable axis grid lines
            ax.yaxis.grid(True)
            ax.xaxis.grid(True)
            fig.subplots_adjust(bottom=0.25, top=0.8)
            ax.set_facecolor(itr['plot_c'])
            fig.patch.set_facecolor(itr['bac_c'])

            fig.savefig('assets/section_2_3_1_{0}.png'.format(numPages))
            numPages+=1


    sectionData = {'num_plts_sec_max_hourly': numPages}
    return sectionData

def fetchSection2_3_MinContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_2_3_2:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    month_name = dt.datetime.strftime(startDt, "%b' %y")
    full_month_name = dt.datetime.strftime(startDt, "%B %Y")
    constituentinfo=getConstituentsMappings()
    numPages = 0

    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrDemVals = mRepo.getEntityMetricHourlyData(
        'wr', 'Demand(MW)', startDt, endDt)

    wrUnResDemDf = pd.DataFrame(wrDemVals)
    wrUnResDemDf = wrUnResDemDf.set_index('time_stamp')

    wr_max_unres_dem = round(wrUnResDemDf['data_value'].min())
    minUnresDemDt = wrUnResDemDf['data_value'].idxmin()

    minDtSrtT=dt.datetime(minUnresDemDt.year,minUnresDemDt.month,minUnresDemDt.day)
    minDtEndT=dt.datetime(minUnresDemDt.year,minUnresDemDt.month,minUnresDemDt.day,23)
    wr_min_unres_dem_time_str = "HOURLY MIN.DEMAND CURVES ON REGIONAL MINIMUM DAY {1} at {0} Hrs".format(dt.datetime.strftime(
        minUnresDemDt, "%H:%M"), dt.datetime.strftime(minUnresDemDt, "%d-%b-%y"))
    wrUnResDemDf= wrUnResDemDf[ (wrUnResDemDf.index>=minDtSrtT) & (wrUnResDemDf.index<=minDtEndT)]

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 2.5))
    # set plot title
    pltTitle="WR"
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('HOUR')
    ax.set_ylabel('MW')
    ax.set_facecolor("violet")
    fig.patch.set_facecolor('#95d0fc')



    wrUnResDemDf.reset_index(inplace=True)
    dateList = []
    times = wrUnResDemDf["time_stamp"]
    for col in times:
            dateList.append(dt.datetime.strftime(col, '%H'))

    wrUnResDemDf["time_stamp"] = dateList
    # plot data and get the line artist object in return
    laThisMonth, = ax.plot(wrUnResDemDf['time_stamp'],
                        wrUnResDemDf['data_value'], color='#0000ff')


    # enable axis grid lines
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.suptitle(wr_min_unres_dem_time_str, fontsize=10)
    fig.savefig('assets/section_2_3_2_{0}.png'.format(numPages))
    numPages+= 1

    for itr in constituentinfo:
        if itr['entity_tag']=='wr':
            continue
        else:

            # get WR Unrestricted demand hourly values for this month and prev yr month
            constDemVals = mRepo.getEntityMetricHourlyData(
                itr['entity_tag'], 'Demand(MW)', minDtSrtT, minDtEndT)

            constUnResDemDf = pd.DataFrame(constDemVals)
            constUnResDemDf = constUnResDemDf.set_index('time_stamp')
            constUnResDemDf.reset_index(inplace=True)
            dateList = []
            times = constUnResDemDf["time_stamp"]
            for col in times:
                dateList.append(dt.datetime.strftime(col, '%H'))

            constUnResDemDf["time_stamp"] = dateList

            # create a plotting area and get the figure, axes handle in return
            fig, ax = plt.subplots(figsize=(7.5, 2.5))
            # set plot title
            pltTitle = itr['display_name']
            ax.set_title(pltTitle)
            # set x and y labels
            ax.set_xlabel('HOUR')
            ax.set_ylabel('MW')
            laThisMonth, = ax.plot(constUnResDemDf['time_stamp'],
                                   constUnResDemDf['data_value'], color='#0000ff')
            # enable axis grid lines
            ax.yaxis.grid(True)
            ax.xaxis.grid(True)
            fig.subplots_adjust(bottom=0.25, top=0.8)
            ax.set_facecolor(itr['plot_c'])
            fig.patch.set_facecolor(itr['bac_c'])
            fig.savefig('assets/section_2_3_2_{0}.png'.format(numPages))
            numPages+=1

    sectionData = {'num_plts_sec_min_hourly': numPages}
    return sectionData
