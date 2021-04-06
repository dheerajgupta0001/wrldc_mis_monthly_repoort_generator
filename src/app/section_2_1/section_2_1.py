import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.config.appConfig import getREConstituentsMappings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math
from src.utils.durationValues import deriveDurationVals
from src.utils.addMonths import addMonths
import numpy as np 

def fetchSection2_1(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:

    loadDurationCurve = fetchSection2_1_LoadDurationCurve(appDbConnStr ,startDt, endDt)
    frequencyDurationCurve = fetchSection2_1FrequencyDurationCurve(appDbConnStr,startDt,endDt)


    secData :dict = {}

    secData['loadDurationCurve'] = loadDurationCurve
    secData['freqDurationCurve'] = frequencyDurationCurve

    return secData


def fetchSection2_1_LoadDurationCurve(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:
    
    mRepo = MetricsDataRepo(appDbConnStr)

    currentMonthMW = mRepo.getEntityMetricHourlyData('wr','Demand(MW)', startDt , endDt)
    df = pd.DataFrame(currentMonthMW)
    currentMonthMWVals = deriveDurationVals(df['data_value'],10)

    pastMonthMW = mRepo.getEntityMetricHourlyData('wr','Demand(MW)',addMonths(startDt,-1) , addMonths(endDt,-1))
    df = pd.DataFrame(pastMonthMW)
    pastMonthMWVals = deriveDurationVals(df['data_value'],10)

    pastYearMW = mRepo.getEntityMetricHourlyData('wr','Demand(MW)',addMonths(startDt,-12) , addMonths(endDt,-12))
    df = pd.DataFrame(pastYearMW)
    pastYearMWVals = deriveDurationVals(df['data_value'],10)

    pltTitle = 'Load Duration Curve {0}, {1} & {2}'.format(startDt.strftime('%b-%y') , addMonths(startDt,-1).strftime('%b-%y') , addMonths(startDt,-12).strftime('%b-%y'))

    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    ax.set_title(pltTitle)
    ax.set_ylabel('Demand met (MW)')
    ax.set_xlabel('% of time')

    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

    
    ax.plot( currentMonthMWVals['perc_exceeded'],currentMonthMWVals['bins'], color='red',label=dt.datetime.strftime(startDt, '%b-%y'))
    ax.plot( pastMonthMWVals['perc_exceeded'] , pastMonthMWVals['bins'],color='blue', label=addMonths(startDt,-1).strftime('%b-%y'))
    ax.plot( pastYearMWVals['perc_exceeded'] , pastYearMWVals['bins'], color='green', label=addMonths(startDt,-12).strftime('%b-%y'))


    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    ax.legend( loc='best',
                    ncol=4, borderaxespad=0.)


    plt.xticks(np.arange(0,110,10))
    ax.set_xlim(xmin=0 , xmax= 100)
    ax.set_ylim(ymin=35000, ymax=65000)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    
    ax.set_facecolor("#cbffff")

    fig.savefig('assets/section_2_1_loadDurationCurve.png')
    # plt.show()
    # plt.close()

    secData: dict = {}
    return secData


def fetchSection2_1FrequencyDurationCurve(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:

    mRepo = MetricsDataRepo(appDbConnStr)

    frequencyData = mRepo.getRawFreq(startDt,endDt)
    df = pd.DataFrame(frequencyData)
    frequencyDataVals = deriveDurationVals(df['frequency'],0.01)
    
    maxFreq = round(df['frequency'].max(),2)
    minFreq = round(df['frequency'].min(),2)
    meanFreq = round(df['frequency'].mean(),2)

    pltTitle = 'Frequency Duration Curve for {0} Max={1} , Min={2} , Avg={3} '.format(startDt.strftime('%b-%y') , maxFreq,minFreq,meanFreq)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    ax.set_title(pltTitle)
    ax.set_ylabel('Freq (HZ)')
    ax.set_xlabel('% of time')

    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

    
    ax.plot( frequencyDataVals['perc_exceeded'],frequencyDataVals['bins'], color='orange')
    

    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    ax.legend( loc='best',
                    ncol=4, borderaxespad=0.)


    plt.xticks(np.arange(0,110,10))
    ax.set_xlim(xmin=0 , xmax= 100)
    ax.set_ylim(ymin=49.6, ymax=50.4)
    fig.subplots_adjust(bottom=0.25, top=0.8)

    ax.set_facecolor("#ffffcc")
    fig.patch.set_facecolor('#cbcbcb')

    fig.savefig('assets/section_2_2_frequencyDurationCurve.png')
    # plt.show()
    # plt.close()

    secData: dict = {}
    return secData
