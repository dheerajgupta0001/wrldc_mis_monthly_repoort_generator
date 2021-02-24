from src.typeDefs.section_1_6.section_1_6_1 import ISection_1_6_1, IFreqDetails
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.utils.convertDtToDayNumMonth import convertDtToDayNumMonth
import matplotlib.pyplot as plt
import math
import numpy as np


def fetchSection1_6_1Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_6_1:
    monthName = dt.datetime.strftime(startDt, "%b %y")
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR freq Daily values for this month
    freqLessThanBandVals = mRepo.getFreqDailyData('< 49.9', startDt, endDt)
    freqLessVals = [x['data_value'] for x in freqLessThanBandVals]
    freqLessVals = [float(i) for i in freqLessVals]
    freq_max_less_band = max(freqLessVals)
    freq_avg_less_band = sum(freqLessVals)/len(freqLessVals)

    freqBetBandVals = mRepo.getFreqDailyData(
        '>= 49.9 - <= 50.05', startDt, endDt)
    freBetVals = [x['data_value'] for x in freqBetBandVals]
    freBetVals = [float(i) for i in freBetVals]
    freq_max_bet_band = max(freBetVals)
    freq_avg_bet_band = sum(freBetVals)/len(freBetVals)

    freqGreaterThanBandVals = mRepo.getFreqDailyData('> 50', startDt, endDt)
    freGreaterThanVals = [x['data_value'] for x in freqGreaterThanBandVals]
    freGreaterThanVals = [float(i) for i in freGreaterThanVals]
    freq_max_greater_than_band = max(freGreaterThanVals)
    freq_avg_greater_than_band = sum(
        freGreaterThanVals)/len(freGreaterThanVals)

    freqFviVals = mRepo.getFreqDailyData('FVI', startDt, endDt)
    freqFVIVals = [x['data_value'] for x in freqFviVals]
    freqFVIVals = [float(i) for i in freqFVIVals]
    max_fvi = max(freqFVIVals)
    avg_fvi = sum(freqFVIVals)/len(freqFVIVals)

    hrsOutOfBandVals = mRepo.getFreqDailyData(
        'Hrs Out of IEGC', startDt, endDt)
    hrsOutOfBand = [x['data_value'] for x in hrsOutOfBandVals]
    hrsOutOfBand = [float(i) for i in hrsOutOfBand]
    hrs_max_out_of_band = max(hrsOutOfBand)
    hrs_avg_out_of_band = sum(hrsOutOfBand)/len(hrsOutOfBand)

    dailyFdi = [x/24 for x in hrsOutOfBand]
    max_Fdi = max(dailyFdi)
    avg_Fdi = sum(dailyFdi)/len(dailyFdi)

    perc_time_out_of_band = [x*100 for x in dailyFdi]
    max_perc_time = max(perc_time_out_of_band)
    avg_perc_time = sum(perc_time_out_of_band)/len(perc_time_out_of_band)

    freqDailyMaxVals = mRepo.getFreqDailyData('max inst f', startDt, endDt)
    freqMaxVals = [x['data_value'] for x in freqDailyMaxVals]
    freqMaxVals = [float(i) for i in freqMaxVals]
    max_monthly_freq = max(freqMaxVals)

    freqDailyMinVals = mRepo.getFreqDailyData('min inst f', startDt, endDt)
    freqMinVals = [x['data_value'] for x in freqDailyMinVals]
    freqMinVals = [float(i) for i in freqMinVals]
    min_monthly_freq = min(freqMinVals)

    freqDailyAvgVals = mRepo.getFreqDailyData('avg frq', startDt, endDt)
    freqAvgVals = [x['data_value'] for x in freqDailyAvgVals]
    freqAvgVals = [float(i) for i in freqAvgVals]
    avg_monthly_freq = sum(freqAvgVals)/len(freqAvgVals)

    # create plot image for freq profile
    pltLessThanBandObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in freqLessThanBandVals]
    pltBetBandObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in freqBetBandVals]
    pltGreaterThanBandObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in freqGreaterThanBandVals]
    pltFviObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in freqFviVals]
    pltHrsOutOfBandObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in hrsOutOfBandVals]
    pltDailyMaxFreqObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in freqDailyMaxVals]
    pltDailyMinFreqObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in freqDailyMinVals]
    pltDailyAvgFreqObjs = [{'Date': convertDtToDayNumMonth(
        x["time_stamp"]), 'colName': x["metric_name"], 'val': x["data_value"]} for x in freqDailyAvgVals]
    tableDataObjs = pltLessThanBandObjs + pltBetBandObjs + pltGreaterThanBandObjs + \
        pltFviObjs + pltHrsOutOfBandObjs + \
        pltDailyMaxFreqObjs + pltDailyMinFreqObjs + pltDailyAvgFreqObjs

    pltFreqGraphObjs = pltLessThanBandObjs + \
        pltBetBandObjs + pltGreaterThanBandObjs

    tableDataDf = pd.DataFrame(tableDataObjs)
    tableDataDf = tableDataDf.pivot(
        index='Date', columns='colName', values='val')
    tableDataDf.reset_index(inplace=True)
    tableDataDf['fdi'] = dailyFdi

    tableDataDf['out_of_band_perc'] = perc_time_out_of_band

    freqProfileList: ISection_1_6_1["freq_profile"] = []

    for i in tableDataDf.index:
        freqProf: IFreqDetails = {
            'date': tableDataDf['Date'][i],
            'less_than_band': round(float(tableDataDf['< 49.9'][i]), 2),
            'freq_bet_band': round(float(tableDataDf['>= 49.9 - <= 50.05'][i]), 2),
            'out_of_band': round(float(tableDataDf['> 50'][i]), 2),
            'fvi': round(float(tableDataDf['FVI'][i]), 2),
            'out_of_band_perc': round(float(tableDataDf['out_of_band_perc'][i]), 2),
            'hrs_out_of_band': round(float(tableDataDf['Hrs Out of IEGC'][i]), 2),
            'fdi': round(float(tableDataDf['fdi'][i]), 2),
            'freq_daily_max': round(float(tableDataDf['max inst f'][i]), 2),
            'freq_daily_min': round(float(tableDataDf['min inst f'][i]), 2),
            'freq_daily_avg': round(float(tableDataDf['avg frq'][i]), 2)
        }
        freqProfileList.append(freqProf)

    sectionData: ISection_1_6_1 = {
        "freq_profile": freqProfileList,
        "freq_max_less_band": round(freq_max_less_band, 2),
        "freq_avg_less_band": round(freq_avg_less_band, 2),
        "freq_max_bet_band": round(freq_max_bet_band, 2),
        "freq_avg_bet_band": round(freq_avg_bet_band, 2),
        "freq_max_greater_than_band": round(freq_max_greater_than_band, 2),
        "freq_avg_greater_than_band": round(freq_avg_greater_than_band, 2),
        "max_fvi": round(max_fvi, 2),
        "avg_fvi": round(avg_fvi, 2),
        "hrs_max_out_of_band": round(hrs_max_out_of_band, 2),
        "hrs_avg_out_of_band": round(hrs_avg_out_of_band, 2),
        "max_Fdi": round(max_Fdi, 2),
        "avg_Fdi": round(avg_Fdi, 2),
        "max_perc_time": round(max_perc_time, 2),
        "avg_perc_time": round(avg_perc_time, 2),
        "max_monthly_freq": round(max_monthly_freq, 2),
        "min_monthly_freq": round(min_monthly_freq, 2),
        "avg_monthly_freq": round(avg_monthly_freq, 2)
    }

    pltFreqGraphDf = pd.DataFrame(pltFreqGraphObjs)
    pltFreqGraphDf = pltFreqGraphDf.pivot(
        index='Date', columns='colName', values='val')
    pltFreqGraphDf.reset_index(inplace=True)
    # save plot data as excel
    pltFreqGraphDf.to_excel("assets/plot_1_6_2.xlsx", index=True)

    # derive plot title
    pltTitle = 'Frequency Profile for {0}'.format(monthName)

    # create a plotting area and get the figure, axes handle in return
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    # set plot title
    ax.set_title(pltTitle)
    # plot data and get the line artist object in return
    width = 0.4
    plt.bar(pltFreqGraphDf['Date'], freqLessVals,
            width=0.4, color='#ff0066', label='<49.9')

    plt.bar(pltFreqGraphDf['Date'], freBetVals, width,
            bottom=freqLessVals, color='#00cc66', label='49.9-50.05')

    greatorThanBandBottom = list(np.add(freqLessVals, freBetVals))

    plt.bar(pltFreqGraphDf['Date'], freGreaterThanVals, width,
            bottom=greatorThanBandBottom, color='#0086b3', label='>50.05')

    plt.xticks(rotation=90)
    # plt.legend()
    plt.legend(bbox_to_anchor=(0.0, -0.35, 1, 0), loc='lower center',
               ncol=3, mode="expand", borderaxespad=0.)
    fig.subplots_adjust(bottom=0.25, left=0.1, right=0.99)
    fig.savefig('assets/section_1_6_2.png')
    # plt.show()
    return sectionData
