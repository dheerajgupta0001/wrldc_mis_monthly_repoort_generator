# import argparse
import datetime as dt
from src.config.appConfig import getJsonConfig, initConfigs
from src.app.monthlyReportGenerator import MonthlyReportGenerator

initConfigs()

# get app config
appConfig = getJsonConfig()

# get app db connection string from config file
appDbConStr: str = appConfig['appDbConnStr']
outageDbConStr :str = appConfig['outageDbConnStr']

dumpFolder: str = appConfig['dumpFolder']

# generate report word file monthly_rep_template
tmplPath: str = "templates/monthly_rep_template.docx"

# create weekly report
mnthlyRprtGntr = MonthlyReportGenerator(appDbConStr,outageDbConStr)
monthDt = dt.datetime(2021,3,1)
mnthlyRprtGntr.generateMonthlyReport(monthDt, tmplPath, dumpFolder)
print('Report generation Done')
