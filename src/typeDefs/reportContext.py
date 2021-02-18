from typing import TypedDict, List
import datetime as dt
from src.typeDefs.section_1_3.section_1_3_a import ISection_1_3_a


class IReportCxt(TypedDict):
    monthDtObj: dt.datetime
    month_name: str
    last_yr_month_name: str
