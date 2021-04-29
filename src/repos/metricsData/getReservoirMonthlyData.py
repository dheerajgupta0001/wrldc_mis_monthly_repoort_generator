import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.reservoir_section.reservoir_section import IReservoirMonthlyDataRecord


def getReservoirMonthlyData(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IReservoirMonthlyDataRecord]:
    targetColumns = ['extract(year from time_stamp) as yr', 'extract(month from time_stamp) as mon',
                     'max(data_value) AS level_max', 'entity_tag', 'metric_tag']

    metricsFetchSql = """
            select {0}
            from mis_warehouse.reservoir_daily_data sf
            where 
            sf.ENTITY_TAG IN ('Gandhi Sagar Reservoir Level ','Indira sagar Reservoir Level',
						'Kadana Reservoir Level','Koyna Reservoir Level ',
						'Omkareshwar Reservoir Level','Ukai Reservoir Level','ssp')
            and sf.METRIC_TAG IN (' Level mtrs',' Level mtrs ')
            and sf.time_stamp between :1 and :2
            group by extract(year from time_stamp), extract(month from time_stamp), entity_tag, metric_tag
            order by yr, mon
        """.format(','.join(targetColumns))

    # test sql
    # testColumns = ["to_char(time_stamp, 'YYYY-MM') as time_stamp", 'max(data_value) as level_max',
    #                 'entity_tag', 'metric_tag']
    # metricsFetchSql = """
    #         select {0}
    #         from MIS_WAREHOUSE.RESERVOIR_DAILY_DATA rdd
    #         WHERE
    #         entity_tag IN ('Gandhi Sagar Reservoir Level ','Indira sagar Reservoir Level',
    # 					'Kadana Reservoir Level','Koyna Reservoir Level ',
    # 					'Omkareshwar Reservoir Level','Ukai Reservoir Level','ssp')
    #         AND METRIC_TAG IN (' Level mtrs',' Level mtrs ')
    #         group by to_char(time_stamp, 'YYYY-MM'), entity_tag, metric_tag
    #         order by 1
    #     """.format(','.join(testColumns))
    # test ends

    # initialise codes to be returned
    dataRecords: List[IReservoirMonthlyDataRecord] = []
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
        print('Error while fetching reservoir MONTHLY data between dates')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    # iterate through each row to populate result daily rows
    for row in dbRows:
        year_dt: IReservoirMonthlyDataRecord["time_stamp"] = row[colNames.index(
            'YR')]
        month_dt: IReservoirMonthlyDataRecord["time_stamp"] = row[colNames.index(
            'MON')]
        entity: IReservoirMonthlyDataRecord["entity_tag"] = row[colNames.index(
            'ENTITY_TAG')]
        level_max: IReservoirMonthlyDataRecord["metric_tag"] = row[colNames.index(
            'LEVEL_MAX')]
        sampl: IReservoirMonthlyDataRecord = {
            "year": year_dt,
            "month": month_dt,
            "entity_tag": entity,
            "level_max": level_max
        }
        dataRecords.append(sampl)
    return dataRecords
