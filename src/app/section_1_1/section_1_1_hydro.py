from src.typeDefs.section_1_1.section_1_1_hydro import ISection_1_1_hydro
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_hydroContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_hydro:
    mRepo = MetricsDataRepo(appDbConnStr)
    # get hydro mu
    hydroMuVals = mRepo.getEntityMetricDailyData(
        "wr", "Hydro(MU)", startDt, endDt)

    maxHydroMuObj = hydroMuVals[0]
    tot_month_hydro_gen_mu = 0
    for v in hydroMuVals:
        tot_month_hydro_gen_mu += v["data_value"]
        if v["data_value"] > maxHydroMuObj["data_value"]:
            maxHydroMuObj = v
    avg_month_hydro_gen_mu = tot_month_hydro_gen_mu/len(hydroMuVals)
    max_month_hydro_gen_mu = round(maxHydroMuObj["data_value"], 2)
    max_month_hydro_gen_mu_date = dt.datetime.strftime(
        maxHydroMuObj["time_stamp"], "%d-%b-%Y")

    # get hydro mu for last year
    hydroMuLastYrVals = mRepo.getEntityMetricDailyData(
        "wr", "Hydro(MU)", addMonths(startDt, -12), addMonths(endDt, -12))
    tot_last_year_hydro_gen_mu = 0
    for v in hydroMuLastYrVals:
        tot_last_year_hydro_gen_mu += v["data_value"]

    tot_last_year_hydro_gen_mu_perc = round(100 *
                                            (tot_month_hydro_gen_mu - tot_last_year_hydro_gen_mu) /
                                            tot_last_year_hydro_gen_mu, 2)

    tot_last_year_hydro_gen_mu_perc_str = ""
    if tot_last_year_hydro_gen_mu_perc < 0:
        tot_last_year_hydro_gen_mu_perc_str = "reduced by {0}%".format(
            -1*tot_last_year_hydro_gen_mu_perc)
    else:
        tot_last_year_hydro_gen_mu_perc_str = "increased by {0}%".format(
            tot_last_year_hydro_gen_mu_perc)

    secData: ISection_1_1_hydro = {
        "tot_month_hydro_gen_mu": round(tot_month_hydro_gen_mu),
        "tot_last_year_hydro_gen_mu": round(tot_last_year_hydro_gen_mu),
        "tot_last_year_hydro_gen_mu_perc_str": tot_last_year_hydro_gen_mu_perc_str,
        "avg_month_hydro_gen_mu": round(avg_month_hydro_gen_mu),
        "max_month_hydro_gen_mu": round(max_month_hydro_gen_mu),
        "max_month_hydro_gen_mu_date": max_month_hydro_gen_mu_date
    }
    return secData
