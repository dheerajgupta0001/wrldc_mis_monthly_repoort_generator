from typing import TypedDict
import datetime as dt

class ISoFarHighestDataRecord(TypedDict):
    constituent: str
    data_value: float
    data_time:dt.datetime