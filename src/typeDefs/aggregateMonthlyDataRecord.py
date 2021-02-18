from typing import TypedDict
import datetime as dt


class IAggregateDataRecord(TypedDict):
    entity_tag: str
    metric_value: float