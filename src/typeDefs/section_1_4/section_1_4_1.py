from typing import TypedDict, List


class IDemDataRow_1_4_1(TypedDict):
    state_name: str
    catered: str
    ls: str
    freq_corr: str
    pc: str
    tot_dem: str
    peak_date: str
    peak_time: str
    freq_at_peak: str


class ISection_1_4_1(TypedDict):
    dem_data_1_4_1: List[IDemDataRow_1_4_1]
