from typing import TypedDict


class ISection_1_3_b(TypedDict):
    entity: str
    peakReqMW: float
    peakAvailMW: float
    shortage_X: float
    highestReqMW: float
    highestAvailMW: float
    shortage_Y: float
    highestReqMWDateStr: str
    highestAvailMWDateStr: str


# class ISection_1_3_b(TypedDict):
#     energy_req_avail: List[IEnergyDetails]
#     recent_fin_month_name: str
