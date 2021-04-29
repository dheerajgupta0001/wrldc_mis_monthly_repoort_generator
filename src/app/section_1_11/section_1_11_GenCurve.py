import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.config.appConfig import getREConstituentsMappings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

### Generation Curvers of Wind and Wind and Solar Combined

def fetchSection1_11_GenerationCurve(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime):
    windWR = fetchSection1_11_WindGenCurveContext(appDbConnStr ,startDt, endDt)
    solarWR = fetchSection1_11_WindSolarCombinedWR(appDbConnStr ,startDt, endDt)

    secData :dict = {}

    secData['windWR'] = windWR
    secData['solarWR'] = solarWR

    return secData

def fetchSection1_11_WindSolarCombinedWR(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime):
    mRepo = MetricsDataRepo(appDbConnStr)

    hourlyGenerationObj = []  
    hourlyGen = mRepo.getEntityMetricHourlyData('wr','Wind(MW)',startDt,endDt)   
    hourlyGenerationObj.append(hourlyGen)

    hourlyGen = mRepo.getEntityMetricHourlyData('wr','Solar(MW)',startDt,endDt)   
    hourlyGenerationObj.append(hourlyGen)

    if(len(hourlyGenerationObj) > 0):
        pltDataObj:list = []

        for temp in range(len(hourlyGenerationObj)):
            
            pltDataObj = pltDataObj + [{'Hours': x["time_stamp"], 'colName': 'Total Solar' if x['metric_name'] == 'Solar(MW)' else 'Total Wind',
                   'val': x["data_value"]} for x in hourlyGenerationObj[temp] ]
        
        pltDataDf = pd.DataFrame(pltDataObj)

        pltDataDf = pltDataDf.pivot(index='Hours',columns='colName',values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataDf.to_excel("assets/plot_1_11_WindSolarGenCurve.xlsx", index=True)

        pltTitle = 'Wind Gen. & Solar Gen. curve  {0} '.format(startDt.strftime('%b-%y'))

        fig, ax = plt.subplots(figsize=(7.5, 5.6))

        ax.set_title(pltTitle)
        ax.set_ylabel('MW')
        ax.set_xlabel('Time')

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))

        clr = ['#00ccff', '#ff8533']
        for col in range(len(pltDataDf.columns)-1):
            ax.plot(pltDataDf['Hours'], pltDataDf[pltDataDf.columns[col+1]], color=clr[col], label=pltDataDf.columns[col+1])


        ax.yaxis.grid(True)
        ax.legend(bbox_to_anchor=(0.5,-0.46,0.0, 0.0), loc='center',
                      ncol=4, borderaxespad=0.)

    
        plt.xticks(rotation=90)
        ax.set_xlim(xmin=startDt , xmax= endDt)
        fig.subplots_adjust(bottom=0.25, top=0.8)

        fig.savefig('assets/section_1_11_WindSolarGenCurve.png')
        # plt.close()

    secData: dict = {}
    
    return secData
    
def fetchSection1_11_WindGenCurveContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) :
    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    hourlyGenerationObj = []  
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(pd.isna(constInfo['windCapacity'])):
            continue

        hourlyGen = mRepo.getEntityMetricHourlyData(constInfo['entity_tag'],'Wind(MW)',startDt,endDt)   
        hourlyGenerationObj.append(hourlyGen)


    if(len(hourlyGenerationObj) > 0):
        pltDataObj:list = []

        for temp in range(len(hourlyGenerationObj)):
            pltDataObj = pltDataObj + [{'Hours': x["time_stamp"], 'colName': x['entity_tag'],
                   'val': x["data_value"]} for x in hourlyGenerationObj[temp] ]
        
        pltDataDf = pd.DataFrame(pltDataObj)

        pltDataDf = pltDataDf.pivot(index='Hours',columns='colName',values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataDf.to_excel("assets/plot_1_11_windGenCurve.xlsx", index=True)

        pltTitle = 'Wind Gen Curve {0} '.format(startDt.strftime('%b-%y'))

        fig, ax = plt.subplots(figsize=(7.5, 5.6))

        ax.set_title(pltTitle)
        ax.set_ylabel('MW')
        ax.set_xlabel('Time')

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))

        clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff','#00ff88']
        for col in range(1,len(pltDataDf.columns)):
            ax.plot(pltDataDf['Hours'], pltDataDf[pltDataDf.columns[col]], color=clr[col-1], label=pltDataDf.columns[col])


        ax.yaxis.grid(True)
        ax.legend(loc='best',
                      ncol=4, borderaxespad=0.)

    
        plt.xticks(rotation=90)
        ax.set_xlim(xmin=startDt , xmax= endDt)
        fig.subplots_adjust(bottom=0.25, top=0.8)

        fig.savefig('assets/section_1_11_windGenCurve.png')
        # plt.close()

    secData: dict = {}
    
    return secData
