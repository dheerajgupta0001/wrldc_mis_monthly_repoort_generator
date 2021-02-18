import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.soFarHighestDataRecord import ISoFarHighestDataRecord


def updateSoFarHighest(appDbConnStr:str,constituent:str, metricName:str,report_month:dt.datetime,data_value:float,data_time:dt.datetime) -> bool:
    updateSql = """
            update MIS_WAREHOUSE.SO_FAR_HIGHEST_MONTHLY sfh
            set data_value = :0 , data_time = :1
            where 
            sfh.constituent = :2
            sfh.METRIC_NAME = :3
            sfh.report_month = :4
    
        """

    isinsert = False
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(updateSql, (data_value,data_time,constituent,metricName, report_month))
        isinsert = True
    except Exception as err:
        dbRows = []
        print('Error while updating so far highest data for month ',report_month)
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    
    return isinsert
