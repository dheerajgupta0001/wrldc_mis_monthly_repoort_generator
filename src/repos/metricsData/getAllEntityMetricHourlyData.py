import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.metricsDataRecord import IMetricsDataRecord


def getAllEntityMetricHourlyData(appDbConnStr: str, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:

    metricsFetchSql = """
            select entity_tag , max(data_value) as data_value, time_stamp
            from mis_warehouse.state_files_data sfh
            where 
            sfh.METRIC_NAME = :0
            and TRUNC(sfh.time_stamp) between TRUNC(:1) and TRUNC(:2)
            group by entity_tag
            order by entity_tag asc
        """

    # initialise codes to be returned
    dataRecords: List[IMetricsDataRecord] = []
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
        print('Error while fetching all entity hourly data between dates')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    # iterate through each row to populate result outage rows
    for row in dbRows:
        timeStamp: IMetricsDataRecord["time_stamp"] = row[colNames.index(
            'TIME_STAMP')]
        entity: IMetricsDataRecord["entity_tag"] = row[colNames.index(
            'ENTITY_TAG')]
        # metric: IMetricsDataRecord["metric_name"] = row[colNames.index(
        #     'METRIC_NAME')] as i am already passing
        val: IMetricsDataRecord["data_value"] = row[colNames.index(
            'DATA_VALUE')]
        sampl: IMetricsDataRecord = {
            "entity_tag": entity,
            "metric_name": metricName,
            "data_value": val,
            "time_stamp": timeStamp
        }
        dataRecords.append(sampl)
    return dataRecords
