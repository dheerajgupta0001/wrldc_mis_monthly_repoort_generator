from os import read
from src.typeDefs.section_1_1.section_1_1_wind_solar import ISection_1_1_wind_solar
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_WindSolarContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_wind_solar:
    mRepo = MetricsDataRepo(appDbConnStr)
    # get solar mu
    solarMuVals = mRepo.getEntityMetricDailyData(
        "wr", "Solar(MU)", startDt, endDt)
    cgsSolarMuVals = mRepo.getEntityMetricDailyData(
        "wr","CGS Solar(Mus)",startDt , endDt)
    
    tot_month_solar_gen_mu = 0
    for s,c in zip(solarMuVals,cgsSolarMuVals):
        tot_month_solar_gen_mu += s["data_value"] + c["data_value"]
    avg_month_solar_gen_mu = tot_month_solar_gen_mu/len(solarMuVals)

    # get solar mu for last year
    solarMuLastYrVals = mRepo.getEntityMetricDailyData(
        "wr", "Solar(MU)", addMonths(startDt, -12), addMonths(endDt, -12))

    cgsSolarMuLastYrVals = mRepo.getEntityMetricDailyData(
        "wr", "CGS Solar(Mus)", addMonths(startDt, -12), addMonths(endDt, -12))

    tot_last_year_solar_gen_mu = 0
    for s,c in zip(solarMuLastYrVals,cgsSolarMuLastYrVals):
        tot_last_year_solar_gen_mu += s["data_value"] + c["data_value"]

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

    solarMwVals = mRepo.getEntityMetricHourlyData(
        "wr", "Solar(MW)", startDt, endDt)
    maxSolarMwObj = solarMwVals[0]
    for v in solarMwVals:
        if v["data_value"] > maxSolarMwObj["data_value"]:
            maxSolarMwObj = v
    max_month_solar_gen_mw = maxSolarMwObj["data_value"]
    max_month_solar_gen_mw_date = '{0} at {1} hrs'.format(dt.datetime.strftime(
        maxSolarMwObj["time_stamp"], "%d %b %Y"), dt.datetime.strftime(
        maxSolarMwObj["time_stamp"], "%H:%M"))

    # get wind mu
    windMuVals = mRepo.getEntityMetricDailyData(
        "wr", "Wind(MU)", startDt, endDt)
    cgsWindMuVals = mRepo.getEntityMetricDailyData(
        "wr", "CGS Wind(Mus)", startDt, endDt)
    tot_month_wind_gen_mu = 0
    for w,c in zip(windMuVals,cgsWindMuVals):
        tot_month_wind_gen_mu += w["data_value"] + c["data_value"]
    avg_month_wind_gen_mu = tot_month_wind_gen_mu/len(windMuVals)

    # get wind mu for last year
    windMuLastYrVals = mRepo.getEntityMetricDailyData(
        "wr", "Wind(MU)", addMonths(startDt, -12), addMonths(endDt, -12))
    cgsWindMuLastYrVals = mRepo.getEntityMetricDailyData(
        "wr", "CGS Wind(Mus)", addMonths(startDt, -12), addMonths(endDt, -12))
    tot_last_year_wind_gen_mu = 0
    for w,c in zip(windMuLastYrVals,cgsWindMuLastYrVals):
        tot_last_year_wind_gen_mu += w["data_value"] + c["data_value"]

    tot_last_year_wind_gen_mu_perc = round(100 *
                                           (tot_month_wind_gen_mu - tot_last_year_wind_gen_mu) /
                                           tot_last_year_wind_gen_mu, 2)

    tot_last_year_wind_gen_mu_perc_str = ""
    if tot_last_year_wind_gen_mu_perc < 0:
        tot_last_year_wind_gen_mu_perc_str = "reduced by {0}%".format(
            -1*tot_last_year_wind_gen_mu_perc)
    else:
        tot_last_year_wind_gen_mu_perc_str = "increased by {0}%".format(
            tot_last_year_wind_gen_mu_perc)

    windMwVals = mRepo.getEntityMetricHourlyData(
        "wr", "Wind(MW)", startDt, endDt)
    maxWindMwObj = windMwVals[0]
    for v in windMwVals:
        if v["data_value"] > maxWindMwObj["data_value"]:
            maxWindMwObj = v
    max_month_wind_gen_mw = maxWindMwObj["data_value"]
    max_month_wind_gen_mw_date = '{0} at {1} hrs'.format(dt.datetime.strftime(
        maxWindMwObj["time_stamp"], "%d %b %Y"), dt.datetime.strftime(
        maxWindMwObj["time_stamp"], "%H:%M"))

    # create dataframe for solar and wind addition
    resDf = pd.DataFrame(windMwVals+solarMwVals)
    resDf = resDf.pivot(index="time_stamp",
                        columns="metric_name", values="data_value")
    resDf["Renewable"] = resDf["Wind(MW)"] + resDf["Solar(MW)"]
    max_month_ren_gen_mw = resDf["Renewable"].max()
    maxRenDt = resDf["Renewable"].idxmax().to_pydatetime()
    max_month_ren_gen_mw_date = '{0} at {1} hrs'.format(dt.datetime.strftime(
        maxRenDt, "%d %b %Y"), dt.datetime.strftime(maxRenDt, "%H:%M"))
    secData: ISection_1_1_wind_solar = {
        'tot_month_wind_gen_mu': round(tot_month_wind_gen_mu),
        'avg_month_wind_gen_mu': round(avg_month_wind_gen_mu, 1),
        'tot_last_year_wind_gen_mu_perc_str': tot_last_year_wind_gen_mu_perc_str,
        'tot_last_year_wind_gen_mu': round(tot_last_year_wind_gen_mu),
        'max_month_wind_gen_mw': round(max_month_wind_gen_mw),
        'max_month_wind_gen_mw_date': max_month_wind_gen_mw_date,
        'tot_month_solar_gen_mu': round(tot_month_solar_gen_mu),
        'avg_month_solar_gen_mu': round(avg_month_solar_gen_mu, 1),
        'tot_last_year_solar_gen_mu_perc_str': tot_last_year_solar_gen_mu_perc_str,
        'tot_last_year_solar_gen_mu': round(tot_last_year_solar_gen_mu),
        'max_month_solar_gen_mw': round(max_month_solar_gen_mw),
        'max_month_solar_gen_mw_date': max_month_solar_gen_mw_date,
        'max_month_ren_gen_mw': round(max_month_ren_gen_mw),
        'max_month_ren_gen_mw_date': max_month_ren_gen_mw_date
    }
    return secData
