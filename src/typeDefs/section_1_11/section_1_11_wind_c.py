from typing import TypedDict, List


class ISoFarHighestDataRow(TypedDict):
    entity: str
    capacityMW: float
    generationMW: float
    highestGenerationMWDateStr: str
    highestGenerationMWTimeStr: str
    

class ISection_1_11_wind_c(TypedDict):
    so_far_hig_wind_gen: List[ISoFarHighestDataRow]