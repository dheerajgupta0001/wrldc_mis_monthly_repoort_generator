import datetime as dt
from typing import List

from numpy import add
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.typeDefs.section_1_10.section_1_10 import ISection_1_10, IOutageDetails
from statistics import mean 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fetchSection1_10Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_10:
    mRepo = MetricsDataRepo(appDbConnStr)
    plannedMonthlyData = mRepo.getOutageData('PLANNED',startDt,endDt)
    forcedMonthlyData = mRepo.getOutageData('FORCED',startDt,endDt)
    totalMonthlyData = calculateTotal(plannedMonthlyData,forcedMonthlyData)

    plannedMonthlyDataLastMonth =  mRepo.getOutageData('PLANNED',addMonths(startDt,-1),startDt-dt.timedelta(days=1))
    forcedMonthlyDataLastMonth =  mRepo.getOutageData('FORCED',addMonths(startDt,-1),startDt-dt.timedelta(days=1))

    totalMonthlyDataLastMonth =  calculateTotal(plannedMonthlyDataLastMonth,forcedMonthlyDataLastMonth)

    monthArray:list[IOutageDetails] = []
    prevMonthArray:list[IOutageDetails] = []

    monthDates = list(plannedMonthlyData.keys())
    prevMonthDates = list(totalMonthlyDataLastMonth.keys())

    for idx,date in enumerate(monthDates):
        dateFormat = dt.datetime.strptime(str(date),'%Y%m%d')

        dayDetail: IOutageDetails = {
            'idx':idx,
            'date':dateFormat,
            'planned': plannedMonthlyData[date],
            'forced': forcedMonthlyData[date],
            'total': totalMonthlyData[date]
        }
        monthArray.append(dayDetail)
    mx = {
        'idx':max(len(monthDates),len(prevMonthDates)),
        'date':'Max',
        'planned':max(plannedMonthlyData.values()),
        'forced':max(forcedMonthlyData.values()),
        'total':max(totalMonthlyData.values())
    }
    monthArray.append(mx)

    avg = {
        'idx':max(len(monthDates),len(prevMonthDates))+1,
        'date':'AVG',
        'planned':round(mean(plannedMonthlyData.values())),
        'forced':round(mean(forcedMonthlyData.values())),
        'total':round(mean(totalMonthlyData.values()))
    }
    monthArray.append(avg)
    monthDf = pd.DataFrame(monthArray)

    for idx,date in enumerate(prevMonthDates):
        if idx < len(monthDates):
            dateFormat = dt.datetime.strptime(str(monthDates[idx]),'%Y%m%d')
        else:
            dateFormat = ''
        dayDetail: IOutageDetails = {
            'idx':idx,
            'total_pre': totalMonthlyDataLastMonth[date]
        }
        prevMonthArray.append(dayDetail)
    mx = {
        'idx':max(len(monthDates),len(prevMonthDates)),
        'total_pre':max(totalMonthlyDataLastMonth.values())
    }
    prevMonthArray.append(mx)

    
    avg = {
        'idx':max(len(monthDates),len(prevMonthDates))+1,
        'total_pre':round(mean(totalMonthlyDataLastMonth.values()))
    }
    prevMonthArray.append(avg)
    prevMonthDf = pd.DataFrame(prevMonthArray)
    resultDf = monthDf.merge(prevMonthDf, left_on='idx', right_on='idx',how='outer')
    resultDf = resultDf.sort_values(by=['idx'])
    # resultDf['date'] = resultDf['date'].dt.strftime()
    resultDf['dateStr'] = resultDf['date'].apply(lambda x: x.strftime('%d-%b-%Y') if type(x) is dt.datetime else x)

    # if(len(monthDates) < len(prevMonthDates)):
    #     itr = len(monthDates)
    #     while itr <= len(prevMonthDates)-1:
    #         date = prevMonthDates[itr]
    #         dateFormat = dt.datetime.strptime(str(date),'%Y%m%d')
    #         dayDetail:IOutageDetails = {
    #             'date': dateFormat,
    #             'planned': 0,
    #             'forced': 0,
    #             'total': 0,
    #             'total_pre':totalMonthlyDataLastMonth[date]
    #         }
    #         monthArray.append(dayDetail)
    #         itr = itr + 1
        
    # for eachDay in monthArray:
    #     eachDay['date'] = dt.datetime.strftime(eachDay['date'],"%d-%b-%Y")

    
    
    sectionData: ISection_1_10 = {
        "generation_outages": resultDf.to_dict('records')
    }
    
    monthLabel = 'Total - '+ dt.datetime.strftime(startDt,'%b-%Y')
    preMonthLabel = 'Total - '+dt.datetime.strftime(addMonths(startDt,-1),'%b-%Y')

    graphDf = resultDf[~pd.isna(resultDf['date'])]
    graphDf = graphDf.iloc[:-2]
    graphDf.to_excel("assets/generation_outage.xlsx", index=False)
    pltTitle = 'Unit Outage {0}'.format(monthLabel)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.set_title(pltTitle)
    ax.set_ylabel('MW')
    ax.set_xlabel('Date')
    
    ax.set_facecolor("#c0d9f1")

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%Y"))

    ax.plot(graphDf['date'],graphDf['planned'],color='#00ccff',label='Planned')
    ax.plot(graphDf['date'],graphDf['forced'],color='#ff8533',label='Forced')
    ax.plot(graphDf['date'],graphDf['total'],color='#ff0000',label=monthLabel)
    ax.plot(graphDf['date'],graphDf['total_pre'],color='#9900ff',label=preMonthLabel)
    ax.yaxis.grid(True)
    ax.legend(bbox_to_anchor=(0.0,-0.46,1, 0), loc='lower left',
                    ncol=4, borderaxespad=0.)


    plt.xticks(rotation=90)
    # ax.set_xlim( allDatesArray[0], allDatesArray[1] ) 
    fig.subplots_adjust(bottom=0.25, top=0.8)

    fig.savefig('assets/section_1_10_generation_outage.png')
    # plt.show()
    # plt.close()
    return sectionData

def calculateTotal(plannedMonthlyData,forcedMonthlyData):
    size = len(plannedMonthlyData)
    dates = list(plannedMonthlyData.keys())
    total = {}
    for itr in range(size):
        total[dates[itr]] = []
        total[dates[itr]] = plannedMonthlyData[dates[itr]] + forcedMonthlyData[dates[itr]]
    
    return total
