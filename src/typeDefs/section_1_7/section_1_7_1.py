from typing import TypedDict, List
import datetime as dt


class IVoltSummary(TypedDict):
    station: float
    max_vol: float
    min_vol: float
    less_perc: float
    band_perc: float
    more_perc: float
    less_hrs: str
    more_hrs: str
    out_hrs: str
    vdi: float


class ISection_1_7_1(TypedDict):
    voltVdiProfile765: List[IVoltSummary]