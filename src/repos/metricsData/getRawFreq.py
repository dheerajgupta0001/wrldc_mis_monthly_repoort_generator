import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.rawFreqRecord import IRawFreqRecord


def getRawFreq(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IRawFreqRecord]:
    targetColumns = ['TIME_STAMP', 'FREQUENCY']

    metricsFetchSql = """
            select {0}
            from mis_warehouse.raw_frequency f
            where 
            f.time_stamp between :1 and :2
            order by time_stamp asc
        """.format(','.join(targetColumns))

    # initialise codes to be returned
    dataRecords: List[IRawFreqRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (startDt, endDt))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching raw frequency data between dates')
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
        timeStamp: dt.datetime = row[colNames.index(
            'TIME_STAMP')]
        val: float = row[colNames.index(
            'FREQUENCY')]
        sampl: IRawFreqRecord = {
            "time_stamp": timeStamp,
            "frequency": val
        }
        dataRecords.append(sampl)
    return dataRecords
