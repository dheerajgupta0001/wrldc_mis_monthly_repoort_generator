from typing import TypedDict
import datetime as dt

class ISection_1_4_2(TypedDict):
    prev_month_name: str
    wr_max_dem: float
    wr_max_dem_date_str: str
    wr_avg_dem: str
    wr_max_dem_last_year: float
    wr_max_dem_date_str_last_year: str
    wr_avg_dem_last_year: str
    wr_avg_dem_perc_change_last_year: float
    wr_max_dem_perc_change_last_year: float
    wr_max_dem_prev_month: float
    wr_max_dem_date_str_prev_month: str
    wr_avg_dem_prev_month: str
    wr_avg_dem_perc_change_prev_month: float
    wr_max_dem_perc_change_prev_month: float