import datetime as dt
from src.typeDefs.voltDataRecord import IVoltDataRecord
from typing import List
import cx_Oracle


def getDailyVoltDataByLevel(appDbConnStr: str, lvl: int, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IVoltDataRecord]:
    targetColumns = ['DATA_TIME', 'ENTITY_NAME',
                     'VOLT_LEVEL', 'METRIC_NAME', 'DATA_VAL']

    dataFetchSql = """
            select {0}
            from mis_warehouse.daily_volt_metrics dvm
            where 
            dvm.VOLT_LEVEL = :1
            and dvm.METRIC_NAME = :2
            and TRUNC(dvm.data_time) between TRUNC(:3) and TRUNC(:4)
            order by data_time asc
        """.format(','.join(targetColumns))

    # initialise codes to be returned
    dataRecords: List[IVoltDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(dataFetchSql, (lvl,
                                     metricName, startDt, endDt))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching volt metric data between dates')
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

    # iterate through each row to populate result outage rows
    for row in dbRows:
        dataTime: IVoltDataRecord["data_time"] = row[colNames.index(
            'DATA_TIME')]
        entity: IVoltDataRecord["entity_name"] = row[colNames.index(
            'ENTITY_NAME')]
        metric: IVoltDataRecord["metric_name"] = row[colNames.index(
            'METRIC_NAME')]
        val: IVoltDataRecord["data_val"] = row[colNames.index(
            'DATA_VAL')]
        voltLvl: IVoltDataRecord["volt_level"] = row[colNames.index(
            'VOLT_LEVEL')]
        sampl: IVoltDataRecord = {
            "data_val": dataTime,
            "entity_name": entity,
            "metric_name": metric,
            "volt_level": voltLvl,
            "data_val": val
        }
        dataRecords.append(sampl)
    return dataRecords
