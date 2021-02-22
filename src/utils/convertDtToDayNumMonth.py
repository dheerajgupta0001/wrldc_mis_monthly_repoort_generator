import datetime as dt


def convertDtToDayNumMonth(t: dt.datetime) -> str:
    dayNum = dt.datetime.strftime(t,"%d-%b")
    return dayNum
