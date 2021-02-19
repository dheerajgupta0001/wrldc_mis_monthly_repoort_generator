from src.typeDefs.section_1_1.section_1_1_wind_solar import ISection_1_1_wind_solar
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_WindSolarContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_wind_solar:
    # TODO complete this
    mRepo = MetricsDataRepo(appDbConnStr)
    # get hydro mu
    solarMuVals = mRepo.getEntityMetricDailyData(
        "wr", "Solar(MU)", startDt, endDt)

    tot_month_solar_gen_mu = 0
    for v in solarMuVals:
        tot_month_solar_gen_mu += v["data_value"]
    avg_month_solar_gen_mu = tot_month_solar_gen_mu/len(solarMuVals)

    # get solar mu for last year
    solarMuLastYrVals = mRepo.getEntityMetricDailyData(
        "wr", "Solar(MU)", addMonths(startDt, -12), addMonths(endDt, -12))
    tot_last_year_solar_gen_mu = 0
    for v in solarMuLastYrVals:
        tot_last_year_solar_gen_mu += v["data_value"]

    tot_last_year_solar_gen_mu_perc = round(100 *
                                            (tot_month_solar_gen_mu - tot_last_year_solar_gen_mu) /
                                            tot_last_year_solar_gen_mu, 2)

    tot_last_year_solar_gen_mu_perc_str = ""
    if tot_last_year_solar_gen_mu_perc < 0:
        tot_last_year_solar_gen_mu_perc_str = "reduced by {0}%".format(
            -1*tot_last_year_solar_gen_mu_perc)
    else:
        tot_last_year_solar_gen_mu_perc_str = "increased by {0}%".format(
            tot_last_year_solar_gen_mu_perc)

    secData: ISection_1_1_hydro = {
        "tot_month_solar_gen_mu": round(tot_month_solar_gen_mu),
        "tot_last_year_solar_gen_mu": round(tot_last_year_solar_gen_mu),
        "tot_last_year_solar_gen_mu_perc_str": tot_last_year_solar_gen_mu_perc_str,
        "avg_month_hydro_gen_mu": round(avg_month_hydro_gen_mu),
        "max_month_hydro_gen_mu": round(max_month_hydro_gen_mu),
        "max_month_hydro_gen_mu_date": max_month_hydro_gen_mu_date
    }
    return secData
