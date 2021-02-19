from typing import TypedDict, List


class ISoFarHighestDataRow(TypedDict):
    entity: str
    peakReqMW: float
    peakAvailMW: float
    shortage_X: float
    highestReqMW: float
    highestAvailMW: float
    shortage_Y: float
    highestReqMWDateStr: str
    highestAvailMWDateStr: str


class ISection_1_3_b(TypedDict):
    so_far_hig_req_avail: List[ISoFarHighestDataRow]
