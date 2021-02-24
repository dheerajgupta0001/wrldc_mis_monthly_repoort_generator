from typing import TypedDict, List
import datetime as dt


class IScheduleDrawalDetails(TypedDict):
    entity: str
    schedule: float
    drawal: float
    difference: float


class ISection_1_9(TypedDict):
    schedule_drawal: List[IScheduleDrawalDetails]
