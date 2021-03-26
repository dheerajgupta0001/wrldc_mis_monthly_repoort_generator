import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.metricsDataRecord import IOutageDataRecord


def getOutageData(appDbConnStr: str, shutdownType: str,  startDt: dt.datetime, endDt: dt.datetime) -> List[IOutageDataRecord]:
    
    metricsFetchSql = """
            SELECT sum(GONR.INSTALLED_CAPACITY) AS CAPACITY , DATE_KEY FROM REPORTING_WEB_UI_UAT.GEN_OUT_NLDC_REPORT gonr WHERE GONR."TYPE" in :1 AND 
            DATE_KEY BETWEEN :2 AND :3
            GROUP BY DATE_KEY 
            ORDER BY DATE_KEY  asc
        """

    # initialise codes to be returned
    dataRecords: List[IOutageDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        sDate = int(dt.datetime.strftime(startDt,'%Y%m%d'))
        eDate = int(dt.datetime.strftime(endDt,'%Y%m%d'))

        dbCur.execute(metricsFetchSql, (shutdownType,sDate, eDate))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching reservoir daily data between dates')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    #Create a Date Object for each Date to sum capacity for a day 
    monthData = {}
    delta = dt.timedelta(days=1)
    while sDate <= eDate:
        monthData[sDate] = 0
        sDate += 1
    # iterate through each row to populate result daily rows
    for row in dbRows:  
        timeStamp: IOutageDataRecord["time_stamp"] = row[colNames.index(
            'DATE_KEY')]
        capacity: IOutageDataRecord["capacity"] = row[colNames.index(
            'CAPACITY')]
        if capacity is None :
            capacity = 0
        monthData[timeStamp] = round(float(capacity))
        
        
    return monthData