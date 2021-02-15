from typing import TypedDict
import datetime as dt

class IReportCxt(TypedDict):
    monthDtObj: dt.datetime
    month_name: str
    last_yr_month_name: str
    # section 1.1.i
    wr_max_unres_dem: float
    wr_max_unres_dem_time_str: str
    wr_max_unres_dem_perc_inc: float
    wr_max_unres_dem_last_yr: float
    wr_avg_unres_dem: float
    wr_avg_unres_dem_last_yr: float
    wr_avg_unres_dem_perc_inc: float
    # section 1.1.iii
    wr_tot_cons_mu: float
    wr_avg_cons_mu: float
    wr_max_cons_mu: float
    wr_max_cons_date: str
    wr_avg_cons_inc_wrt_last_yr: float
    last_yr_month_str: str
    wr_avg_cons_mu_last_yr: float
    # section 1.1.iv
    wr_tot_req_mu: float
    wr_avg_req_mu: float
    wr_max_req_mu: float
    wr_max_req_date: str
    wr_avg_req_inc_wrt_last_yr: float
    wr_avg_req_mu_last_yr: float
    
