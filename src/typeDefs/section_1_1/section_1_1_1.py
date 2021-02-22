from typing import TypedDict
import datetime as dt

class ISection_1_1_1(TypedDict):
    monthDtObj: dt.datetime
    month_name: str
    full_month_name: str
    last_yr_month_name: str
    wr_max_unres_dem: float
    wr_max_unres_dem_time_str: str
    wr_max_unres_dem_perc_inc: float
    wr_max_unres_dem_last_yr: float
    wr_avg_unres_dem: float
    wr_avg_unres_dem_last_yr: float
    wr_avg_unres_dem_perc_inc: float