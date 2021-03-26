import datetime as dt
from typing import List
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

    plannedMonthlyDataLastMonth =  mRepo.getOutageData('PLANNED',addMonths(startDt,-1),addMonths(endDt,-1))
    forcedMonthlyDataLastMonth =  mRepo.getOutageData('FORCED',addMonths(startDt,-1),addMonths(endDt,-1))

    totalMonthlyDataLastMonth =  calculateTotal(plannedMonthlyDataLastMonth,forcedMonthlyDataLastMonth)

    monthArray:list[IOutageDetails] = []
    monthDates = list(plannedMonthlyData.keys())
    allDatesArray = []
    for date in monthDates:
        dateFormat = dt.datetime.strptime(str(date),'%Y%m%d')

        dateFormatPrev = addMonths(dateFormat,-1)
        datePrev = int(dt.datetime.strftime(dateFormatPrev,'%Y%m%d'))

        allDatesArray.append(dateFormat)

        dayDetail: IOutageDetails = {
            'date': dt.datetime.strftime(dateFormat,'%d-%b-%Y'),
            'planned': plannedMonthlyData[date],
            'forced': forcedMonthlyData[date],
            'total': totalMonthlyData[date],
            'total_pre':totalMonthlyDataLastMonth[datePrev]
        }
        monthArray.append(dayDetail)

    mx = {
        'date':'Max',
        'planned':max(plannedMonthlyData.values()),
        'forced':max(forcedMonthlyData.values()),
        'total':max(totalMonthlyData.values()),
        'total_pre':max(totalMonthlyDataLastMonth.values())
    }
    monthArray.append(mx)

    avg = {
        'date':'AVG',
        'planned':round(mean(plannedMonthlyData.values())),
        'forced':round(mean(forcedMonthlyData.values())),
        'total':round(mean(totalMonthlyData.values())),
        'total_pre':round(mean(totalMonthlyDataLastMonth.values()))
    }
    monthArray.append(avg)
    
    sectionData: ISection_1_10 = {
        "generation_outage": monthArray
    }

    month = dt.datetime.strftime(startDt,'%b-%Y')
    total_col = 'Total-'+month

    df = pd.DataFrame()
    df['Date'] = allDatesArray
    df['Planned'] = plannedMonthlyData.values()
    df['Forced'] = forcedMonthlyData.values()
    df[total_col] =  totalMonthlyData.values()
    df['Total-Prev-Month'] = totalMonthlyDataLastMonth.values()

    df.to_excel("assets/generation_outage.xlsx", index=False)

    pltTitle = 'Unit Outage {0}'.format(month)

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    ax.set_title(pltTitle)
    ax.set_ylabel('MW')
    ax.set_xlabel('Date')

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b-%Y"))

    clr = ['#00ccff', '#ff8533', '#ff0000', '#9900ff']
    for col in range(len(df.columns)-1):
        ax.plot(df['Date'], df[df.columns[col+1]], color=clr[col], label=df.columns[col+1])


    ax.yaxis.grid(True)
    ax.legend(bbox_to_anchor=(0.0,-0.46,1, 0), loc='lower left',
                    ncol=4, borderaxespad=0.)


    plt.xticks(rotation=90)
    # ax.set_xlim( allDatesArray[0], allDatesArray[1] ) 
    fig.subplots_adjust(bottom=0.25, top=0.8)

    fig.savefig('assets/section_1_10_generation_outage.png')
    plt.close()
    return sectionData

def calculateTotal(plannedMonthlyData,forcedMonthlyData):
    size = len(plannedMonthlyData)
    dates = list(plannedMonthlyData.keys())
    total = {}
    for itr in range(size):
        total[dates[itr]] = []
        total[dates[itr]] = plannedMonthlyData[dates[itr]] + forcedMonthlyData[dates[itr]]
    
    return total