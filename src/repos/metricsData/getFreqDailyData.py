import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.metricsDataRecord import IFreqMetricsDataRecord


def getFreqDailyData(appDbConnStr: str, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IFreqMetricsDataRecord]:
    targetColumns = ['DATA_TIME', 'METRIC_NAME', 'DATA_VAL']

    metricsFetchSql = """
            select {0}
            from mis_warehouse.daily_freq_metrics sf
            where 
            sf.METRIC_NAME = :1
            and TRUNC(sf.data_time) between TRUNC(:2) and TRUNC(:3)
            order by data_time asc
        """.format(','.join(targetColumns))

    # initialise codes to be returned
    dataRecords: List[IFreqMetricsDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (metricName, startDt, endDt))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching daily frequency data between dates')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return []

    # iterate through each row to populate result daily rows
    for row in dbRows:
        timeStamp: IFreqMetricsDataRecord["time_stamp"] = row[colNames.index(
            'DATA_TIME')]
        metric: IFreqMetricsDataRecord["metric_name"] = row[colNames.index(
            'METRIC_NAME')]
        val: IFreqMetricsDataRecord["data_value"] = row[colNames.index(
            'DATA_VAL')]
        sampl: IFreqMetricsDataRecord = {
            "time_stamp": timeStamp,
            "metric_name": metric,
            "data_value": val
        }
        dataRecords.append(sampl)
    return dataRecords
