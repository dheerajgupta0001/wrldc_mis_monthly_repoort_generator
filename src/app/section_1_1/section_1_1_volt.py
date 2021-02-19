from src.typeDefs.section_1_1.section_1_1_volt import ISection_1_1_volt
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd


def fetchSection1_1_voltContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_volt:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    month_name = dt.datetime.strftime(startDt, "%b %y")
    mRepo = MetricsDataRepo(appDbConnStr)
    # get high voltage violation data for 765 kV
    voltData765 = mRepo.getDailyVoltDataByLevel(
        765, "%Time >420 or 800", startDt, endDt)
    # convert to dataframe
    voltData765Df = pd.DataFrame(voltData765)
    # take only required columns
    voltData765Df = voltData765Df[["entity_name", "data_val"]]
    # convert column to numeric
    voltData765Df['data_val'] = pd.to_numeric(
        voltData765Df['data_val'], errors='coerce')
    # get mean for each substation
    voltData765Df = voltData765Df.groupby("entity_name").mean()
    voltData765Df.reset_index(inplace=True)
    # check if there is violation more than 0.1
    is765MoreThan10Perc = voltData765Df[voltData765Df["data_val"]
                                        > 10].shape[0] > 0
    msg765 = ""
    if not is765MoreThan10Perc:
        msgStations = voltData765Df[voltData765Df["data_val"]
                                    > 0]["entity_name"].values
        msgStations = [x.replace(' - 765KV', '').capitalize()
                       for x in msgStations]
        msg765 = "All 765 kV nodes of WR were within the IEGC limit."
        if len(msgStations) > 0:
            msg765 = "All 765 kV nodes of WR were within the IEGC limit except few instances at {0}.".format(
                ','.join(msgStations))
    else:
        msgStations = voltData765Df[voltData765Df["data_val"]
                                    > 10]["entity_name"].values
        msgStations = [x.replace(' - 765KV', '').capitalize()
                       for x in msgStations]
        highViolSubstation = voltData765Df.loc[voltData765Df['data_val'].idxmax(
        )]
        msg765 = "High Voltage (greater than 800 kV) at 765 kV substations were observed at {0}. Highest of {1}{2} of time voltage remained above 780 kV at {3} in the month of {4}.".format(
            ', '.join(msgStations), round(highViolSubstation["data_val"], 2), "%", highViolSubstation["entity_name"].replace(' - 765KV', '').capitalize(), month_name)

    # get high voltage violation data for 400 kV
    voltData400 = mRepo.getDailyVoltDataByLevel(
        400, "%Time >420 or 800", startDt, endDt)
    # convert to dataframe
    voltData400Df = pd.DataFrame(voltData400)
    # take only required columns
    voltData400Df = voltData400Df[["entity_name", "data_val"]]
    # convert column to numeric
    voltData400Df['data_val'] = pd.to_numeric(
        voltData400Df['data_val'], errors='coerce')
    # get mean for each substation
    voltData400Df = voltData400Df.groupby("entity_name").mean()
    voltData400Df.reset_index(inplace=True)
    # check if there is violation more than 0.1
    is400MoreThan10Perc = voltData400Df[voltData400Df["data_val"]
                                        > 10].shape[0] > 0
    msg400 = ""
    if not is400MoreThan10Perc:
        msgStations = voltData400Df[voltData400Df["data_val"]
                                    > 0]["entity_name"].values
        msgStations = [x.replace(' - 400KV', '').capitalize()
                       for x in msgStations]
        msg400 = "All 400 kV nodes of WR were within the IEGC limit."
        if len(msgStations) > 0:
            msg400 = "All 400 kV nodes of WR were within the IEGC limit except few instances at {0}.".format(
                ','.join(msgStations))
    else:
        msgStations = voltData400Df[voltData400Df["data_val"]
                                    > 10]["entity_name"].values
        msgStations = [x.replace(' - 400KV', '').capitalize()
                       for x in msgStations]
        highViolSubstation = voltData400Df.loc[voltData400Df['data_val'].idxmax(
        )]
        msg400 = "High Voltage (greater than 420 kV) at 400 kV substations were observed at {0}. Highest of {1}{2} of time voltage remained above 420 kV at {3} in the month of {4}.".format(
            ', '.join(msgStations), round(highViolSubstation["data_val"], 2), "%", highViolSubstation["entity_name"].replace(' - 400KV', '').capitalize(), month_name)
    msg = " ".join([msg765, msg400])
    secData: ISection_1_1_volt = {
        "msg_1_1_volt": msg
    }
    return secData
