from typing import TypedDict
import datetime as dt


class ISection_1_1_hydro(TypedDict):
    tot_month_hydro_gen_mu: float
    tot_last_year_hydro_gen_mu: float
    tot_last_year_hydro_gen_mu_perc_str: str
    avg_month_hydro_gen_mu: float
    max_month_hydro_gen_mu: float
    max_month_hydro_gen_mu_date: str
