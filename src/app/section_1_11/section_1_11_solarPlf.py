import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
from src.config.appConfig import getREConstituentsMappings
import numpy as np
from src.typeDefs.section_1_11.section_1_11_PLFCUF import ISection_1_11_PLFCUF, IPLFCUFDataRow
import math

def fetchSection1_11_solarPLF(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_11_PLFCUF:
    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    numOfDays = ( endDt - startDt ).days + 1

    soFarHighestAllEntityGenVals = mRepo.getSoFarHighestAllEntityData(
        'soFarHighestSolarGen', addMonths(startDt, -1))
    soFarHighestGenLookUp = {}
    for v in soFarHighestAllEntityGenVals:
        soFarHighestGenLookUp[v['constituent']] = {
            'value': v['data_value'], 'ts': v['data_time']}

    dispRows: List[IPLFCUFDataRow] = []
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['solarCapacity'])):
            continue

        maxGenData = mRepo.getEntityMetricHourlyData(
            constInfo["entity_tag"], "Solar(MW)", startDt, endDt)
        
        if constInfo['entity_tag'] == 'central':
            solarEnerConsumption = mRepo.getEntityMetricDailyData(
            'wr', 'CGS Solar(Mus)' ,startDt, endDt)
        else:   
            solarEnerConsumption = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'], 'Solar(MU)' ,startDt, endDt)
        
        energyConsumption = mRepo.getEntityMetricDailyData(
            constInfo['entity_tag'],'Consumption(MU)',startDt , endDt
        )

        maxGenDf = pd.DataFrame(maxGenData)
        maxGenDf = maxGenDf.pivot(
            index='time_stamp',columns='metric_name',values='data_value'
        )
        solarEnerConsumptionSum = pd.DataFrame(solarEnerConsumption).groupby('entity_tag').sum().iloc[0]['data_value']

        if(len(energyConsumption) == 0):
            # THis is for central sector as we don't have consumption data
            # calculate mu from mw
            # df = pd.DataFrame(maxGenData)
            # average = df.groupby('entity_tag').mean()
            # solarEnerConsumptionSumDf = average * 0.024 * numOfDays #To Calculate Avg MU from MW
            # solarEnerConsumptionSum = solarEnerConsumptionSumDf.iloc[0]['data_value']
            EnerConsumptionSum = 0
            penetrationLevel = 0
        else:
            # solarEnerConsumptionSum = pd.DataFrame(solarEnerConsumption).groupby('entity_tag').sum().iloc[0]['data_value']
            EnerConsumptionSum = pd.DataFrame(energyConsumption).groupby('entity_tag').sum().iloc[0]['data_value']
            penetrationLevel = round((solarEnerConsumptionSum/EnerConsumptionSum) * 100 ,2)

        maxSolar = maxGenDf["Solar(MW)"].max()
        maxSolarDt = maxGenDf["Solar(MW)"].idxmax()


        plf = ( solarEnerConsumptionSum * 1000 ) / (int(constInfo['solarCapacity'])*24*numOfDays )
        cuf = maxSolar * 100 / (int(constInfo['solarCapacity']))

        prevHighestSolarObj = soFarHighestGenLookUp[constInfo["entity_tag"]]
        newHighestSolar = maxSolar
        newHighestSolarTime = maxSolarDt.to_pydatetime()

        if newHighestSolar < prevHighestSolarObj["value"]:
            newHighestSolar = prevHighestSolarObj["value"]
            newHighestSolarTime = prevHighestSolarObj["ts"]

               
        mRepo.insertSoFarHighest(
            constInfo['entity_tag'], "soFarHighestSolarGen", startDt, newHighestSolar, newHighestSolarTime)
        # soFarHighestAllEntityGenVals = mRepo.getSoFarHighestAllEntityData(
        # 'soFarHighestSolarGen', startDt)
        # soFarHighestGenLookUp = {}
        # for v in soFarHighestAllEntityGenVals:
        #     soFarHighestGenLookUp[v['constituent']] = {
        #     'value': v['data_value'], 'ts': v['data_time']}
        
        so_far_high_gen_str = str(round(newHighestSolar)) + ' on ' + dt.datetime.strftime(newHighestSolarTime,'%d-%b-%Y') + ' at ' + dt.datetime.strftime(newHighestSolarTime,'%H:%S')
                              
        const_display_row: IPLFCUFDataRow = {
            'entity': constInfo['display_name'],
            'capacityMW': round(constInfo['solarCapacity']),
            'maxgenerationMW': round(maxSolar),
            'soFarHighestGenMW': so_far_high_gen_str,
            'energyGeneration': round(solarEnerConsumptionSum),
            'energyConsumption': round(EnerConsumptionSum),
            'penetration': penetrationLevel,
            'plf': round(plf*100),
            'cuf': round(cuf)                                                           
        }
        dispRows.append(const_display_row)

    secData: ISection_1_11_PLFCUF = {"so_far_hig_solar_gen_plf": dispRows}
    return secData
