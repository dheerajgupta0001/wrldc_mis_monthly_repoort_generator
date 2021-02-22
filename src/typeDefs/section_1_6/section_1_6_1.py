from typing import TypedDict, List
import datetime as dt


class IFreqDetails(TypedDict):
    date: str
    less_than_band: float
    freq_bet_band: float
    out_of_band: float
    fvi: float
    out_of_band_perc: float
    hrs_out_of_band: float
    fdi: float
    freq_daily_max: float
    freq_daily_min: float
    freq_daily_avg: float


class ISection_1_6_1(TypedDict):
    freq_profile: List[IFreqDetails]
    freq_max_less_band: float
    freq_avg_less_band: float
    freq_max_bet_band: float
    freq_avg_bet_band: float
    freq_max_greater_than_band: float
    freq_avg_greater_than_band: float
    max_fvi: float
    avg_fvi: float
    hrs_max_out_of_band: float
    hrs_avg_out_of_band: float
    max_Fdi: float
    avg_Fdi: float
    max_perc_time: float
    avg_perc_time: float
    max_monthly_freq: float
    min_monthly_freq: float
    avg_monthly_freq: float