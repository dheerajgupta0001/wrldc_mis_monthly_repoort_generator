# import argparse
import datetime as dt
from src.config.appConfig import getJsonConfig, initConfigs
from src.app.monthlyReportGenerator import MonthlyReportGenerator

initConfigs()

# get app config
appConfig = getJsonConfig()

# get app db connection string from config file
appDbConStr: str = appConfig['appDbConnStr']
dumpFolder: str = appConfig['dumpFolder']

<<<<<<< HEAD
# generate report word file
tmplPath: str = "assests/monthly_rep_template.docx"
=======
# generate report word file monthly_rep_template
tmplPath: str = "templates/monthly_rep_template.docx"
>>>>>>> efaf8445d5581d145bd19e16b88feb316c470437

# create weekly report
mnthlyRprtGntr = MonthlyReportGenerator(appDbConStr)
monthDt = dt.datetime(2021,1,1)
mnthlyRprtGntr.generateMonthlyReport(monthDt, tmplPath, dumpFolder)
print('Report generation Done')
