from typing import TypedDict
import datetime as dt

class ISection_1_5_3(TypedDict):
    prev_month_name: str
    wr_avg_con: str
    wr_avg_con_prev_month: str
    wr_avg_con_last_year: str
    wr_avg_con_perc_change_prev_month: float
    wr_avg_con_perc_change_last_year: float
    wr_max_con: float
    wr_max_con_prev_month: float
    wr_max_con_last_year: float
    wr_max_con_perc_change_prev_month: float
    wr_max_con_perc_change_last_year: float
    wr_max_con_date_str: str
    wr_max_con_date_str_prev_month: str
    wr_max_con_date_str_last_year: str