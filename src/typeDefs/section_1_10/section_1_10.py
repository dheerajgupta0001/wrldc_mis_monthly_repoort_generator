from typing import TypedDict, List
import datetime as dt


class IOutageDetails(TypedDict):
    date: str
    planned: int
    forced: int
    total: int
    total_pre:int


class ISection_1_10(TypedDict):
    unit_outage: List[IOutageDetails]
