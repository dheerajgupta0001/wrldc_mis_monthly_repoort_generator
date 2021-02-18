import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.aggregateMonthlyDataRecord import IAggregateDataRecord


def getAllEntityMetricMonthlyData(appDbConnStr: str, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IAggregateDataRecord]:
    # targetColumns = ['TIME_STAMP', 'ENTITY_TAG', 'METRIC_NAME', 'DATA_VALUE']

    metricsFetchSql = """
            select entity_tag, sum(data_value) as metric_value
            from mis_warehouse.state_files_daily_data sf
            where 
            sf.METRIC_NAME = :0
            and TRUNC(sf.time_stamp) between TRUNC(:1) and TRUNC(:2)
            GROUP BY entity_tag
            order by entity_tag asc
        """

    # initialise codes to be returned
    dataRecords: List[IAggregateDataRecord] = []
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
        print('Error while fetching daily data between dates')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    # iterate through each row to populate result daily rows
    for row in dbRows:
        entity: IAggregateDataRecord["entity_tag"] = row[colNames.index(
            'ENTITY_TAG')]
        metric: IAggregateDataRecord["metric_name"] = row[colNames.index(
            'METRIC_VALUE')]
        sampl: IAggregateDataRecord = {
            "entity_tag": entity,
            "metric_value": metric
        }
        dataRecords.append(sampl)
    return dataRecords
