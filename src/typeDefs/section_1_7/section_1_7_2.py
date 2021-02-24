from typing import TypedDict, List
from src.typeDefs.section_1_7.section_1_7_1 import IVoltSummary


class ISection_1_7_2(TypedDict):
    voltVdiProfile400: List[IVoltSummary]
