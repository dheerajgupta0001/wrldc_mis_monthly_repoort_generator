from typing import TypedDict
import datetime as dt


class IVoltDataRecord(TypedDict):
    data_time: dt.datetime
    entity_name: str
    volt_level:str
    metric_name: str
    data_val: float