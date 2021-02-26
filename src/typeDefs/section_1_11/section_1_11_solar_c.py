from typing import TypedDict, List


class ISoFarHighestDataRow(TypedDict):
    entity: str
    capacityMW: float
    generationMW: float
    highestGenerationMWDateStr: str
    highestGenerationMWTimeStr: str
<<<<<<< HEAD
    
=======

>>>>>>> origin

class ISection_1_11_solar_c(TypedDict):
    so_far_hig_solar_gen: List[ISoFarHighestDataRow]
