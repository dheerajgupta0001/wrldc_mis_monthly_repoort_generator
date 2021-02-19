from typing import TypedDict


class ISection_1_1_wind_solar(TypedDict):
    tot_month_wind_gen_mu: float
    avg_month_wind_gen_mu: float
    tot_last_year_wind_gen_mu_perc_str: str
    tot_last_year_wind_gen_mu: float
    max_month_wind_gen_mw: float
    max_month_wind_gen_mw_date: str
    tot_month_solar_gen_mu: float
    avg_month_solar_gen_mu: float
    tot_last_year_solar_gen_mu_perc_str: str
    tot_last_year_solar_gen_mu: float
    max_month_solar_gen_mw: float
    max_month_solar_gen_mw_date: str
    max_month_ren_gen_mw: float
    max_month_ren_gen_mw_date: str
