import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.soFarHighestDataRecord import ISoFarHighestDataRecord


def insertSoFarHighest(appDbConnStr: str, constituent: str, metricName: str, report_month: dt.datetime, data_value: float, data_time: dt.datetime) -> bool:
    insertSql = """
            insert into MIS_WAREHOUSE.SO_FAR_HIGHEST_MONTHLY sfh
            (constituent , metric_name , report_month , data_value, data_time)
            values (:1,:2,:3,:4,:5)
        """

    isInserted = False
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()

        existingEntityRecords = (constituent, metricName , report_month )
                                
        dbCur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
        dbCur.execute("Delete from MIS_WAREHOUSE.SO_FAR_HIGHEST_MONTHLY where constituent:=1 and metric_name= :2 and report_month = :3" , existingEntityRecords)
        dbCur.execute(insertSql, (data_value, data_time,
                                  constituent, metricName, report_month))
        isInserted = True
    except Exception as err:
        print('Error while inserting so far highest data for month ', report_month)
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    return isInserted
