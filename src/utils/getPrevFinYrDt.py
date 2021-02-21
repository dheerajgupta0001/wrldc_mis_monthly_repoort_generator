import datetime as dt
from src.utils.addMonths import addMonths


def getPrevFinYrDt(t: dt.datetime):
    t2 = addMonths(t, -1)
    if not t2.month == 4:
        t2 = addMonths(t2, -1)
        while not t2.month == 4:
            t2 = addMonths(t2, -1)
        return t2
    return t2
