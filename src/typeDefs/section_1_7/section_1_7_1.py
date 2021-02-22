from typing import TypedDict, List
import datetime as dt


class IVoltSummary(TypedDict):
    s_no: str
    station_name: float
    max_vol: float
    min_vol: float
    vol_less_band_perc: float
    vol_in_band_perc: float
    vol_more_band_perc: float
    vol_less_band_hrs: str
    vol_more_band_hrs: str
    vol_out_band_hrs: str
    vdi: float


class ISection_1_7_1(TypedDict):
    voltProfile: List[IVoltSummary]
