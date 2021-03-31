from src.typeDefs.section_1_1.section_1_1_freq import ISection_1_1_freq
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_freq_Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_freq:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    mRepo = MetricsDataRepo(appDbConnStr)
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrFreqBetBandVals = mRepo.getFreqDailyData('>= 49.9 - <= 50.05', startDt, endDt)
    wrFreqBetBandDf = pd.DataFrame(wrFreqBetBandVals)
    wrFreqBetBandDf.set_index('time_stamp', inplace=True)
    wrFreqBetBandDf['data_value'] = pd.to_numeric(wrFreqBetBandDf['data_value'])
    bet_band = round(wrFreqBetBandDf['data_value'].mean(), 3)

    wrAvgFreqVals = mRepo.getFreqDailyData('avg frq', startDt, endDt)
    wrAvgFreqDf = pd.DataFrame(wrAvgFreqVals)
    wrAvgFreqDf.set_index('time_stamp', inplace=True)
    wrAvgFreqDf['data_value'] = pd.to_numeric(wrAvgFreqDf['data_value'])
    avg_freq = round(wrAvgFreqDf['data_value'].mean(), 3)

    wrFdiVals = mRepo.getFreqDailyData('FDI', startDt, endDt)
    wrFdiVals = pd.DataFrame(wrFdiVals)
    wrFdiVals['data_value'] = pd.to_numeric(wrFdiVals['data_value'])
    fdi = round(wrFdiVals['data_value'].mean(), 3)
    # print(fdi)

    wrMaxFreqVals = mRepo.getFreqDailyData('max inst f', startDt, endDt)
    wrMaxFreqDf = pd.DataFrame(wrMaxFreqVals)
    wrMaxFreqDf.set_index('time_stamp', inplace=True)
    wrMaxFreqDf['data_value'] = pd.to_numeric(wrMaxFreqDf['data_value'])
    wrMaxFreqDate = wrMaxFreqDf['data_value'].idxmax()
    max_freq = round(wrMaxFreqDf['data_value'].max(), 2)

    wrMaxFreqTimeVals = mRepo.getFreqDailyData('time max f', startDt, endDt)
    wrMaxFreqTimeDf = pd.DataFrame(wrMaxFreqTimeVals)
    wrMaxFreqTimeDf.set_index('time_stamp', inplace=True)
    # wrMaxFreqDate = dt.datetime.strftime(wrMaxFreqDate, "%Y-%m-%d %H:%M:%S")
    wrMaxFreqTime = wrMaxFreqTimeDf.loc[wrMaxFreqDate]['data_value']

    max_freq_time_str = "{0} at {1}".format(dt.datetime.strftime(
        wrMaxFreqDate, "%d-%b-%y"), wrMaxFreqTime)

    wrMinFreqVals = mRepo.getFreqDailyData('min inst f', startDt, endDt)
    wrMinFreqDf = pd.DataFrame(wrMinFreqVals)
    wrMinFreqDf.set_index('time_stamp', inplace=True)
    wrMinFreqDf['data_value'] = pd.to_numeric(wrMinFreqDf['data_value'])
    wrMinFreqDate = wrMinFreqDf['data_value'].idxmin()
    min_freq = round(wrMinFreqDf['data_value'].min(), 3)

    wrMinFreqTimeVals = mRepo.getFreqDailyData('time min f', startDt, endDt)
    wrMinFreqTimeDf = pd.DataFrame(wrMinFreqTimeVals)
    wrMinFreqTimeDf.set_index('time_stamp', inplace=True)
    wrMinFreqTime = wrMinFreqTimeDf.loc[wrMinFreqDate]['data_value']

    min_freq_time_str = "{0} at {1}".format(dt.datetime.strftime(
        wrMinFreqDate, "%d-%b-%y"), wrMinFreqTime)

    
    secData: ISection_1_1_freq = {
        'bet_band': bet_band,
        'avg_freq': avg_freq,
        'fdi': fdi,
        'max_freq': max_freq,
        'max_freq_time_str': max_freq_time_str,
        'min_freq': min_freq,
        'min_freq_time_str': min_freq_time_str

    }
    return secData
