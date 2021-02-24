from typing import TypedDict
import datetime as dt


class IRawFreqRecord(TypedDict):
    time_stamp: dt.datetime
    frequency: float
