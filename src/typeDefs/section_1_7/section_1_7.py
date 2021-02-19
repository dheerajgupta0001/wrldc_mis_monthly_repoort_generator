from typing import TypedDict,List
import datetime as dt



class IVoltageRecord(TypedDict):
    station_name:str
    max_voltage:int
    min_voltage:int
    less_than_728:float
    btwn_728_800:float
    more_than_800:float
    hrs_below_728:dt.datetime
    hrs_above_800:dt.datetime
    hrs_in_IEGC_range:dt.datetime
    vdi:dt.datetime


class ISection_1_7(TypedDict):
    voltage_record:List[IVoltageRecord]