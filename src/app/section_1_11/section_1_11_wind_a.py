import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.config.appConfig import getREConstituentsMappings
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

def fetchSection1_11_Wind_A(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:

    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['windCapacity'])):
            continue
        
        windEnerGeneration = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'], 'Wind(MU)' ,startDt, endDt)
        

    # create plot image for generation of prev fin year and this fin year
        # pltGenerationObjs = [{'MONTH': x["time_stamp"], 'colName': finYrName,
        #            'val': x["data_value"]} for x in windEnerGeneration]

    
    
        pltDataDf = pd.DataFrame(windEnerGeneration)

    # save plot data as excel
        pltDataDf.to_excel("assets/plot_1_11_wind_a.xlsx", index=True)

    # derive plot title
    pltTitle = 'Total Wind Generation (MUs) {0} '.format(startDt.strftime('%b-%y'))

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # set plot title
    ax.set_title(pltTitle)
    # set x and y labels
    ax.set_xlabel('Days')
    ax.set_ylabel('MUs')

    plt.xticks(rotation=90)
    # set x axis formatter as month name and 10 days interval
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b') )
    
    ax.set_xlim(xmin=prevFinYrStart , xmax= finYrStart-dt.timedelta(days=1))
    
    # plot data and get the line artist object in return
    laThisYr, = ax.plot(pltDataDf.index.values,
                        pltDataDf[finYrName].values, color='#ff0000' )
    laThisYr.set_label(finYrName)

    laLastYear, = ax.plot(pltDataDf.index.values,
                          pltDataDf[prevFinYrName].values, color='#0000ff')
    laLastYear.set_label(prevFinYrName)

    # enable axis grid lines
    ax.yaxis.grid(True)
    ax.xaxis.grid(True)
    # enable legends
    ax.legend(bbox_to_anchor=(0.0, -0.3, 0.4, 0.0), loc='lower center',
              ncol=2, borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, top=0.8)
    fig.savefig('assets/section_1_11_solar.png')

    secData: dict = {}
    return secData
