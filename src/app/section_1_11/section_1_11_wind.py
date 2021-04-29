import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.config.appConfig import getREConstituentsMappings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

def fetchSection1_11_Wind(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:

    windA = fetchSection1_11_Wind_A(appDbConnStr ,startDt, endDt)
    windB = fetchSection1_11_Wind_B(appDbConnStr ,startDt, endDt)

    secData :dict = {}

    secData['windA'] = windA
    secData['windB'] = windB

    return secData


def fetchSection1_11_Wind_B(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:
    
    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    allEntitySoFarHighest = mRepo.getSoFarHighestAllEntityData('soFarHighestWindGen',startDt)
    wrSoFarHighest = {}
    for itr in range(len(allEntitySoFarHighest)):
        if allEntitySoFarHighest[itr]['constituent'] == 'wr':
            wrSoFarHighest = allEntitySoFarHighest[itr]
    
    soFarHighestDate = wrSoFarHighest['data_time']

    hourlyGenerationObj = []    
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['windCapacity'])):
            continue

        hourlyGen = mRepo.getEntityMetricHourlyData(constInfo['entity_tag'],'Wind(MW)',soFarHighestDate,soFarHighestDate)   
        hourlyGenerationObj.append(hourlyGen) 

    if(len(hourlyGenerationObj) > 0):
        pltDataObj:list = []

        for temp in range(len(hourlyGenerationObj)):
            pltDataObj = pltDataObj + [{'Hours': x["time_stamp"].hour, 'colName': x['entity_tag'],
                   'val': x["data_value"]} for x in hourlyGenerationObj[temp] ]
        
        pltDataDf = pd.DataFrame(pltDataObj)

        pltDataDf = pltDataDf.pivot(index='Hours',columns='colName',values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataDf.to_excel("assets/plot_1_11_wind_2.xlsx", index=True)

        pltTitle = 'Highest Wind Generation on {0} '.format(soFarHighestDate.strftime('%d-%m-%y'))

        fig, ax = plt.subplots(figsize=(7.5, 4.5))

        ax.set_title(pltTitle)
        ax.set_ylabel('MW')
        ax.set_xlabel('Hours')

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

        clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff','#00ff88']
        for col in range(len(pltDataDf.columns)-1):
            ax.plot(pltDataDf['Hours'], pltDataDf[pltDataDf.columns[col+1]], color=clr[col], label=pltDataDf.columns[col+1])


        ax.yaxis.grid(True)
        ax.legend(bbox_to_anchor=(0.5,-0.3,0.0, 0.0), loc='center',
                      ncol=4, borderaxespad=0.)

    
        # plt.xticks(rotation=90)
        ax.set_xlim(xmin=0 , xmax= 23)
        fig.subplots_adjust(bottom=0.25, top=0.8)

        fig.savefig('assets/section_1_11_wind_2.png')
        # plt.close()

    secData: dict = {}
    return secData
def fetchSection1_11_Wind_A(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:

    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)
    windDataObj:list = []
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['windCapacity'])):
            continue
        
        windEnerGeneration = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'], 'Wind(MU)' ,startDt, endDt)

        windDataObj.append(windEnerGeneration)
    
    if(len(windDataObj) > 0):
        pltDataObj:list = []
        
        for temp in range(len(windDataObj)):
            pltDataObj = pltDataObj + [{'Date': x["time_stamp"], 'colName': x['entity_tag'],
                   'val': x["data_value"]} for x in windDataObj[temp] ]
        
        pltDataDf = pd.DataFrame(pltDataObj)
    
        pltDataDf = pltDataDf.pivot(index='Date',columns='colName',values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataDf.to_excel("assets/plot_1_11_wind_1.xlsx", index=True)

        pltTitle = 'Total Wind Generation (MUs) {0} '.format(startDt.strftime('%b-%y'))

        fig, ax = plt.subplots(figsize=(7.5, 5.5))

        ax.set_title(pltTitle)
        ax.set_ylabel('Mus')
        ax.set_xlabel('Date')

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y'))

        clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff','#ff3300']
        for col in range(1,len(pltDataDf.columns)):
            ax.plot(pltDataDf['Date'], pltDataDf[pltDataDf.columns[col]], color=clr[col-1], label=pltDataDf.columns[col])


        ax.yaxis.grid(True)
        ax.legend(bbox_to_anchor=(0.5,-0.4,0.0, 0.0), loc='center',
                      ncol=4, borderaxespad=0.)

    
        plt.xticks(rotation=90)
        ax.set_xlim(xmin=startDt , xmax= endDt)
        fig.subplots_adjust(bottom=0.25, top=0.8)

        fig.savefig('assets/section_1_11_wind_1.png')
        # plt.close()

    secData: dict = {}
    return secData
