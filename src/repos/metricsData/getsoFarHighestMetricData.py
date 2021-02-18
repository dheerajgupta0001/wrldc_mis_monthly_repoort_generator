import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.soFarHighestDataRecord import ISoFarHighestDataRecord


def getSoFarHighestAllEntityData(appDbConnStr: str, metricName: str, report_month:dt.datetime  ) -> List[ISoFarHighestDataRecord]:

    metricsFetchSql = """
            select constituent , data_value , data_time 
            from MIS_WAREHOUSE.SO_FAR_HIGHEST_MONTHLY sfh
            where 
            sfh.METRIC_NAME = :1
            and TRUNC(sfh.report_month) = :2
            GROUP BY constituent
            order by constituent asc
        """

    # initialise codes to be returned
    dataRecords: List[ISoFarHighestDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (metricName, report_month))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching so far highest data for month ',report_month)
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    # iterate through each row to populate so far highest rows
    for row in dbRows:
        constituent: ISoFarHighestDataRecord['constituent'] = row[colNames.index(
            'constituent')]
        data_value: ISoFarHighestDataRecord['data_value'] = row[colNames.index(
            'data_value')]
        data_time: ISoFarHighestDataRecord['data_time'] = row[colNames.index(
            'data_time')]

        sampl: ISoFarHighestDataRecord = {
            "constituent": constituent,
            "data_value": data_value,
            "data_time":data_time
        }
        dataRecords.append(sampl)
    return dataRecords
