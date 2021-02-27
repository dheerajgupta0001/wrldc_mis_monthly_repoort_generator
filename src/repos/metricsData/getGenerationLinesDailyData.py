import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.metricsDataRecord import IGenerationLinesDataRecord


def getGenerationLinesDailyData(appDbConnStr: str, entityName: str, generatorName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IGenerationLinesDataRecord]:
    targetColumns = ['TIME_STAMP', 'ENTITY_TAG', 'GENERATOR_TAG', 'DATA_VALUE']

    metricsFetchSql = """
            select {0}
            from mis_warehouse.GEN_LINES_DAILY_DATA sf
            where 
            sf.ENTITY_TAG = :1
            and sf.GENERATOR_TAG = :2
            and TRUNC(sf.time_stamp) between TRUNC(:3) and TRUNC(:4)
            order by time_stamp asc
        """.format(','.join(targetColumns))

    # initialise codes to be returned
    dataRecords: List[IGenerationLinesDataRecord] = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql, (entityName,
                                        generatorName, startDt, endDt))

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while fetching generation lines data between dates')
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
        timeStamp: IGenerationLinesDataRecord["time_stamp"] = row[colNames.index(
            'TIME_STAMP')]
        entity: IGenerationLinesDataRecord["entity_tag"] = row[colNames.index(
            'ENTITY_TAG')]
        generator: IGenerationLinesDataRecord["generator_tag"] = row[colNames.index(
            'GENERATOR_TAG')]
        val: IGenerationLinesDataRecord["data_value"] = row[colNames.index(
            'DATA_VALUE')]
        sampl: IGenerationLinesDataRecord = {
            "time_stamp": timeStamp,
            "entity_tag": entity,
            "generator_tag": generator,
            "data_value": val
        }
        dataRecords.append(sampl)
    return dataRecords
