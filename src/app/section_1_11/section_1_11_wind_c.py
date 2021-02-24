import datetime as dt
from typing import List
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
from src.config.appConfig import getREConstituentsMappings
from src.typeDefs.section_1_11.section_1_11_wind_c import ISoFarHighestDataRow, ISection_1_11_wind_c
import math

def fetchSection1_11_wind_cContext(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_11_wind_c:
    constituentsInfos = getREConstituentsMappings()
    mRepo = MetricsDataRepo(appDbConnStr)

    soFarHighestAllEntityVals = mRepo.getSoFarHighestAllEntityData(
        'soFarHighestWindGen', addMonths(startDt, -1))
    soFarHighestWindLookUp = {}
    for v in soFarHighestAllEntityVals:
        soFarHighestWindLookUp[v['constituent']] = {
            'value': v['data_value'], 'ts': v['data_time']}

    dispRows: List[ISoFarHighestDataRow] = []
    for cIter in range(len(constituentsInfos)):
        constInfo = constituentsInfos[cIter]

        if(math.isnan(constInfo['windCapacity'])):
            continue

        highestGenerationDateTime = soFarHighestWindLookUp[constInfo['entity_tag']]['ts']

        const_display_row: ISoFarHighestDataRow = {
            'entity': constInfo['display_name'],
            'capacityMW': constInfo['windCapacity'],
            'generationMW': soFarHighestWindLookUp[constInfo['entity_tag']]['value'],
            'highestGenerationMWDateStr': dt.datetime.strftime(highestGenerationDateTime, "%d.%m.%Y"),
            'highestGenerationMWTimeStr': dt.datetime.strftime(highestGenerationDateTime, "%H:%M")
        }
        dispRows.append(const_display_row)

    secData: ISection_1_11_wind_c = {"so_far_hig_wind_gen": dispRows}
    return secData
