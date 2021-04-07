from typing import Dict
import pandas as pd
import datetime as dt

from typing import List


def getRRASData(targetFilePath: str, startDt:dt.datetime , endDt: dt.datetime) :
    rrasUp = []
    rrasDown = []

    dataSheet = ''
    # find the sheet that has data
    sheetName = startDt.strftime("%b'%y")
    targetFilePath = targetFilePath + 'RRAS '+sheetName+' REPORT.xlsx'
    df = pd.read_excel(targetFilePath, sheet_name=sheetName , header=2, usecols='B:H')
    
    upRecords = df.iloc[0:34]
    downRecords = df.iloc[38:72 , :5]

    dfRecords = {}

    dfRecords['up'] = upRecords
    dfRecords['down'] = downRecords
    return dfRecords
