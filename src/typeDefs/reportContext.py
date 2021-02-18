from typing import TypedDict, List
import datetime as dt
from src.typeDefs.section_1_3.section_1_3_a import ISection_1_3_a

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
    # section 1.1.ii
    wr_peak_dem_met: float
    wr_peak_dem_time_str: str
    wr_peak_dem_perc_inc: float
    wr_last_year_peak_dem: float
    wr_avg_dem: float
    wr_avg_dem_last_yr: float
    wr_avg_dem_perc_inc: float
    # section 1.1.iii
    wr_tot_cons_mu: float
    wr_avg_cons_mu: float
    wr_max_cons_mu: float
    wr_max_cons_mu_date: str
    wr_avg_cons_mu_perc_inc: float
    wr_avg_cons_mu_last_yr: float
    # section 1.1.iv
    wr_tot_req_mu: float
    wr_avg_req_mu: float
    wr_max_req_mu: float
    wr_max_req_mu_date: str
    wr_avg_req_mu_perc_inc: float
    wr_avg_req_mu_last_yr: float

    # section 1.3.a
    energy_req_avail: List[ISection_1_3_a]