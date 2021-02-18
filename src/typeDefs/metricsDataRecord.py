from typing import TypedDict
import datetime as dt


class IMetricsDataRecord(TypedDict):
    time_stamp: dt.datetime
    entity_tag: str
    metric_name: str
    data_value: float

class IFreqMetricsDataRecord(TypedDict):
    time_stamp: dt.datetime
    metric_name: str
    data_value: float