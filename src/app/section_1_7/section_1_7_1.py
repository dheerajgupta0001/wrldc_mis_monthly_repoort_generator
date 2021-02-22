from src.typeDefs.section_1_7.section_1_7_1 import ISection_1_7_1
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd


def fetchSection1_7_1Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_7_1:
    mRepo = MetricsDataRepo(appDbConnStr)

    # get voltage data for this month
    maxVoltData = mRepo.getDailyVoltDataByLevel(765, "Max", startDt, endDt)
    maxVoltDf = pd.DataFrame(maxVoltData)
    maxVoltDf["data_val"] = pd.to_numeric(
        maxVoltDf["data_val"], errors='coerce')
    maxVoltDf = maxVoltDf[["entity_name", "data_val"]
                          ].groupby("entity_name").max()

    minVoltData = mRepo.getDailyVoltDataByLevel(765, "Min", startDt, endDt)
    minVoltDf = pd.DataFrame(minVoltData)
    minVoltDf["data_val"] = pd.to_numeric(
        minVoltDf["data_val"], errors='coerce')
    minVoltDf = minVoltDf[["entity_name", "data_val"]
                          ].groupby("entity_name").min()
    sectionData: ISection_1_7_1 = {
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

    return sectionData
