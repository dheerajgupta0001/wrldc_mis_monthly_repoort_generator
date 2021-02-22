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
