from typing import TypedDict, List
import datetime as dt


class IEnergyDetails(TypedDict):
    entity: str
    reqMu_X: float
    availMu_X: float
    shortage_X: float
    reqMu_Y: float
    availMu_Y: float
    shortage_Y: float


class ISection_1_3_a(TypedDict):
    energy_req_avail: List[IEnergyDetails]
    recent_fin_month_name: str
