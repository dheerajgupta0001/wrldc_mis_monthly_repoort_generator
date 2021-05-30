import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.config.appConfig import getREConstituentsMappings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

def fetchSection1_11_SolarGen(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:

    solarA = fetchSection1_11_Solar_A(appDbConnStr ,startDt, endDt)
    solarB = fetchSection1_11_Solar_B(appDbConnStr ,startDt, endDt)

    secData :dict = {}

    secData['solarA'] = solarA
    secData['solarB'] = solarB
    secData['wr_solar_so_far_highest'] = solarB
    return secData


def fetchSection1_11_Solar_B(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:
    
    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    allEntitySoFarHighest = mRepo.getSoFarHighestAllEntityData('soFarHighestSolarGen',startDt)
    wrSoFarHighest = {}
    for itr in range(len(allEntitySoFarHighest)):
        if allEntitySoFarHighest[itr]['constituent'] == 'wr':
            wrSoFarHighest = allEntitySoFarHighest[itr]
    
    soFarHighestDate = wrSoFarHighest['data_time']

    hourlyGenerationObj = []    
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['solarCapacity'])):
            continue

        hourlyGen = mRepo.getEntityMetricHourlyData(constInfo['entity_tag'],'Solar(MW)',soFarHighestDate,soFarHighestDate)   
        hourlyGenerationObj.append(hourlyGen) 

    if(len(hourlyGenerationObj) > 0):
        pltDataObj:list = []

        for temp in range(len(hourlyGenerationObj)):
            pltDataObj = pltDataObj + [{'Hours': x["time_stamp"].hour, 'colName': x['entity_tag'],
                   'val': x["data_value"]} for x in hourlyGenerationObj[temp] ]
        
        pltDataDf = pd.DataFrame(pltDataObj)

        pltDataDf = pltDataDf.pivot(index='Hours',columns='colName',values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataDf.to_excel("assets/plot_1_11_solar_2.xlsx", index=True)

        pltTitle = 'Highest Solar Generation on {0} '.format(soFarHighestDate.strftime('%d-%m-%y'))

        fig, ax = plt.subplots(figsize=(7.5, 4.5))

        ax.set_title(pltTitle)
        ax.set_ylabel('MW')
        ax.set_xlabel('Hours')

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))

        clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff','#00ff88','#3388ff']
        for col in range(len(pltDataDf.columns)-1):
            ax.plot(pltDataDf['Hours'], pltDataDf[pltDataDf.columns[col+1]], color=clr[col], label=pltDataDf.columns[col+1])


        ax.yaxis.grid(True)
        ax.legend(bbox_to_anchor=(0.5,-0.3,0.0, 0.0), loc='center',
                      ncol=4, borderaxespad=0.)

    
        # plt.xticks(rotation=90)
        ax.set_xlim(xmin=0 , xmax= 23)
        fig.subplots_adjust(bottom=0.25, top=0.8)

        fig.savefig('assets/section_1_11_solar_2.png')
        # plt.close()

    secData: dict = { 'data' : wrSoFarHighest['data_value'] , 'date': dt.datetime.strftime(wrSoFarHighest['data_time'],'%d.%m.%Y') ,'time':dt.datetime.strftime(wrSoFarHighest['data_time'],'%H:%M')}
    return secData
def fetchSection1_11_Solar_A(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:

    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)
    solarDataObj:list = []
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['solarCapacity'])):
            continue

        if(constInfo['entity_tag'] == 'wr'):
            solarEnerGeneration = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'], 'Solar(MU)' ,startDt, endDt)
            cgsSolarGeneration = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'], 'CGS Solar(Mus)' ,startDt, endDt)
            
            for s,c in zip(solarEnerGeneration,cgsSolarGeneration):
                s['data_value'] += c['data_value']

        elif constInfo['entity_tag'] == 'central':
            solarEnerGeneration = mRepo.getEntityMetricDailyData(
            'wr', 'CGS Solar(Mus)' ,startDt, endDt)
            for c in solarEnerGeneration:
                c['entity_tag'] = 'central'
        
        else:
            solarEnerGeneration = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'], 'Solar(MU)' ,startDt, endDt)

        solarDataObj.append(solarEnerGeneration)
    
    if(len(solarDataObj) > 0):
        pltDataObj:list = []
        
        for temp in range(len(solarDataObj)):
            pltDataObj = pltDataObj + [{'Date': x["time_stamp"], 'colName': x['entity_tag'],
                   'val': x["data_value"]} for x in solarDataObj[temp] ]
        
        pltDataDf = pd.DataFrame(pltDataObj)
    
        pltDataDf = pltDataDf.pivot(index='Date',columns='colName',values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataDf.to_excel("assets/plot_1_11_solar_1.xlsx", index=True)

        pltTitle = 'Total Solar Generation (MUs) {0} '.format(startDt.strftime('%b-%y'))

        fig, ax = plt.subplots(figsize=(7.5, 5.5))

        ax.set_title(pltTitle)
        ax.set_ylabel('Mus')
        ax.set_xlabel('Date')

        ax.set_facecolor("#ffffdc")

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y'))

        clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff','#ff3300','#44ff66']
        for col in range(1,len(pltDataDf.columns)):
            ax.plot(pltDataDf['Date'], pltDataDf[pltDataDf.columns[col]], color=clr[col-1], label=pltDataDf.columns[col])


        ax.yaxis.grid(True)
        ax.legend(loc='best',
                      ncol=4, borderaxespad=0.)

    
        plt.xticks(rotation=90)
        ax.set_xlim(xmin=startDt , xmax= endDt)
        fig.subplots_adjust(bottom=0.25, top=0.8)

        fig.savefig('assets/section_1_11_solar_1.png')
        # plt.show()
        # plt.close()


    secData: dict = {}
    return secData
