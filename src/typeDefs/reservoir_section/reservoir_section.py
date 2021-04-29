from typing import TypedDict, List
import datetime as dt


class IReservoirSection(TypedDict):
    num_plts_sec_reservoir: int 

class IReservoirMonthlyDataRecord(TypedDict):
    year: dt.datetime
    month: dt.datetime
    metric_tag: str
    level_max: float

class IReservoirMonthlyTableDataRecord(TypedDict):
    date_time: dt.datetime
    gandhi: float
    indira: float
    omkare: float
    kadana: float
    ssp: float
    ukai: float
    koyna: float

class ISection_reservoir_table(TypedDict):
    reservoir_table: List[IReservoirMonthlyTableDataRecord]