import datetime as dt
import cx_Oracle
from typing import List


def getEntityREHourlyData(appDbConnStr: str, entityName: str, startDt: dt.datetime, endDt: dt.datetime) :
    

    metricsFetchSql = """
            SELECT TIME_STAMP , sum(data_value) AS val FROM MIS_WAREHOUSE.STATE_FILES_DATA sfd
    WHERE sfd.ENTITY_TAG  = :1 AND 
    sfd.METRIC_NAME IN ('Solar(MW)','Wind(MW)' ) AND 
    TRUNC(sfd.TIME_STAMP) BETWEEN TRUNC(:2) AND TRUNC(:3)
    GROUP  BY TIME_STAMP 
    ORDER  BY TIME_STAMP  ASC
        """

    # initialise codes to be returned
    dataRecords  = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (entityName, startDt, endDt))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching hourly data between dates')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

   

    # iterate through each row to populate result outage rows
    for row in dbRows:
        timeStamp = row[colNames.index('TIME_STAMP')]
        
        val =  row[colNames.index('VAL')]
        sampl= {
            "time_stamp": timeStamp,
            "val": val
        }
        dataRecords.append(sampl)
    return dataRecords
