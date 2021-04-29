import datetime as dt
from typing import List, Any
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.utils.getPrevFinYrDt import getPrevFinYrDt
import pandas as pd
from src.config.appConfig import getReservoirsMappings
from src.utils.convertDtToDayNumMonth import convertDtToDayNumMonthYear
import math
from src.typeDefs.reservoir_section.reservoir_section import IReservoirMonthlyDataRecord, ISection_reservoir_table


def fetchReservoirMonthlyTableContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> IReservoirMonthlyDataRecord:
    # reservoirInfo = getReservoirsMappings()

    mRepo = MetricsDataRepo(appDbConnStr)
    finYrStartDt = getPrevFinYrDt(startDt)
    mRepo = MetricsDataRepo(appDbConnStr)
    reservoirMonthlyVals = mRepo.getReservoirMonthlyData(finYrStartDt, endDt)
    reservoirMonthlyDf = pd.DataFrame(reservoirMonthlyVals)
    reservoirMonthlyDf['day'] = 1
    # loadDurationCurve = fetchSection2_1_LoadDurationCurve(appDbConnStr ,startDt, endDt)
    reservoirMonthlyDf['Date'] = pd.to_datetime(reservoirMonthlyDf[['year', 'month', 'day']])
    # reservoirMonthlyDf['Date'] = reservoirMonthlyDf['Date'].dt.strftime('%d-%m-%y')
    reservoirMonthlyDf = reservoirMonthlyDf.drop(['year', 'month', 'day'], axis=1)
    reservoirMonthlyDf = reservoirMonthlyDf.pivot(
                index='Date', columns='entity_tag', values='level_max')
    reservoirMonthlyDf = reservoirMonthlyDf.rename(columns={
                    'Gandhi Sagar Reservoir Level ': 'a_gandhi_sagar',
                    'Indira sagar Reservoir Level': 'a_indira_sagar',
                    'Omkareshwar Reservoir Level': 'a_omkareshwar',
                    'Kadana Reservoir Level': 'b_kadana',
                    'ssp': 'b_ssp',
                    'Ukai Reservoir Level': 'b_ukai',
                    'Koyna Reservoir Level ': 'c_koyna'
                    })
    
    reservoirMonthlyDf = reservoirMonthlyDf.reindex(sorted(reservoirMonthlyDf.columns), axis=1)
    reservoirMonthlyDf.reset_index(inplace=True)
    reservoirMonthlyDf['Date'] = reservoirMonthlyDf['Date'].dt.strftime('%b %y')
    # reservoirMonthlyDf = reservoirMonthlyDf.drop(['Date'], axis=1)
    print("testing")

    reservoirTableList: ISection_reservoir_table["schedule_drawal"] = []

    for i in reservoirMonthlyDf.index:
        reservoirTableRecord: IReservoirMonthlyDataRecord = {
            # 'date_time': dt.datetime.strftime(reservoirMonthlyDf['Date'][i], '%d-%m-%Y'),
            'date_time': reservoirMonthlyDf['Date'][i],
            'gandhi': reservoirMonthlyDf['a_gandhi_sagar'][i],
            'indira': round(reservoirMonthlyDf['a_indira_sagar'][i]),
            'omkare': round(reservoirMonthlyDf['a_omkareshwar'][i]),
            'kadana': round(reservoirMonthlyDf['b_kadana'][i]),
            'ssp': round(reservoirMonthlyDf['b_ssp'][i]),
            'ukai': round(reservoirMonthlyDf['b_ukai'][i]),
            'koyna': round(reservoirMonthlyDf['c_koyna'][i])
        }
        reservoirTableList.append(reservoirTableRecord)
    
    sectionData: ISection_reservoir_table = {
        "reservoir_table": reservoirTableList
    }

    return sectionData
