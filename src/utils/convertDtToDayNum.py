import datetime as dt


def convertDtToDayNum(t: dt.datetime) -> float:
    dayNum = t.day + (t.hour/24) + (t.minute/(24*60))
    return dayNum
