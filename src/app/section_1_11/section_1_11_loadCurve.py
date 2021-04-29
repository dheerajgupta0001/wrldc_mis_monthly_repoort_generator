import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.config.appConfig import getREConstituentsMappings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def fetchSection1_11_LoadCurve(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime):
    mRepo = MetricsDataRepo(appDbConnStr)

    pltDataObj:list = []

    totalGen = mRepo.getEntityREHourlyData('wr',startDt, endDt)
    df = pd.DataFrame(totalGen)   
    
    
    max_total_gen_position = df['val'].idxmax()
    max_total_gen_dt = df['time_stamp'].iloc[max_total_gen_position]
    max_str_date  = dt.datetime(max_total_gen_dt.year,max_total_gen_dt.month,max_total_gen_dt.day)

    totalGenOnMaxGenDay = mRepo.getEntityREHourlyData('wr',max_str_date,max_str_date)
    wrDemandOnMaxGenDay = mRepo.getEntityMetricHourlyData('wr','Demand(MW)',max_str_date,max_str_date)

    pltDataDf = pd.DataFrame()
    pltDataDf['hours'] = [x['time_stamp'].hour+1 for x in totalGenOnMaxGenDay]
    pltDataDf['reGen'] = [ x['val'] for x in totalGenOnMaxGenDay]
    pltDataDf['wrDemand'] = [ x['data_value'] for x in wrDemandOnMaxGenDay]
    pltDataDf['netLoad'] = [ float(x['data_value']) - float(y['val']) for x,y in zip(wrDemandOnMaxGenDay,totalGenOnMaxGenDay)]

    pltDataDf.to_excel("assets/plot_1_11_netloadcurve.xlsx")

    pltTitle = 'Net load Curve when RES (wind and Solar) Generation was max on {0} '.format(max_str_date.strftime('%d-%m-%Y'))

    fig, ax = plt.subplots(figsize=(7.5, 5.6))

    ax.set_title(pltTitle)
    ax.set_ylabel('MW')
    ax.set_xlabel('Hour')

    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

    clr = ['#03a56a','#a5033e', '#00ffff']
    x = pltDataDf['hours']
    y = [ pltDataDf['reGen'] , pltDataDf['netLoad'] ,pltDataDf['wrDemand'] ]

    # ax.stackplot(x, y , labels=['Wind+Solar' ,'Net Load', 'WR Demand'],baseline='sym')

    ax.fill_between(x,y[0],color='red',alpha=0.5,label='Wind+Solar')
    ax.fill_between(x,y[1],color='blue',alpha=0.5,label='Net Load')
    ax.fill_between(x,y[2],color='black',alpha=0.5,label='WR Demand')

    ax.yaxis.grid(True)
    ax.legend(bbox_to_anchor=(0.5,-0.2,0.0, 0.0), loc='center',
                      ncol=4, borderaxespad=0.)

    
    # plt.xticks(rotation=90)
    ax.set_xlim(xmin=1 , xmax= 24)
    fig.subplots_adjust(bottom=0.25, top=0.8)

    fig.savefig('assets/section_1_11_netLoadCurve.png')
    # plt.close()

    secData: dict = {}
    
    return secData
    
