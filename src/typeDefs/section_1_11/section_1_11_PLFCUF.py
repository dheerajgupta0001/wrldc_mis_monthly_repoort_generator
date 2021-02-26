from typing import TypedDict, List


class IPLFCUFDataRow(TypedDict):
    entity: str
    capacityMW: float
    maxgenerationMW: float
    soFarHighestGenMW:str
    energyGeneration:float
    energyConsumption:float
    penetration:float
    plf:float
    cuf:float

    

class ISection_1_11_PLFCUF(TypedDict):
    so_far_hig_plf_cuf: List[IPLFCUFDataRow]
