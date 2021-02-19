from typing import TypedDict
import datetime as dt

class ISection_1_1_freq(TypedDict):
    bet_band: float
    avg_freq: float
    fdi: float
    max_freq: float
    max_freq_time_str: str
    min_freq: float
    min_freq_time_str: float