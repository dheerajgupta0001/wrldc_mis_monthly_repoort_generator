import os
import datetime as dt
from src.typeDefs.reportContext import IReportCxt
from typing import List
from docxtpl import DocxTemplate, InlineImage
from src.app.section_1_1.section_1_1_1 import fetchSection1_1_1Context
from src.app.section_1_1.section_1_1_2 import fetchSection1_1_2Context
from src.app.section_1_1.section_1_1_3 import fetchSection1_1_3Context
from src.app.section_1_1.section_1_1_4 import fetchSection1_1_4Context
from src.app.section_1_4.section_1_4_2 import fetchSection1_4_2Context
from src.utils.addMonths import addMonths
# from docx2pdf import convert


class MonthlyReportGenerator:
    appDbConStr: str = ''

    def __init__(self, appDbConStr: str):
        self.appDbConStr = appDbConStr

    def getReportContextObj(self, monthDt: dt.datetime) -> IReportCxt:
        """get the report context object for populating the weekly report template
        Args:
            monthDt (dt.datetime): month date object
        Returns:
            IReportCxt: report context object
        """
        # create context for weekly report
        reportContext: IReportCxt = {}

        startDt = dt.datetime(monthDt.year, monthDt.month, 1)
        endDt = addMonths(startDt, 1) - dt.timedelta(days=1)
        # get section 1.1.1 data
        try:
            secData_1_1_1 = fetchSection1_1_1Context(
                self.appDbConStr, startDt, endDt)
            reportContext.update(secData_1_1_1)
            print(
                "section 1_1_1 context setting complete")
        except Exception as err:
            print(
                "error while fetching section 1_1_1")
            print(err)

        # get section 1.1.2 data
        try:
            secData_1_1_2 = fetchSection1_1_2Context(
                self.appDbConStr, startDt, endDt
            )
            reportContext.update(secData_1_1_2)
            print(
                "section 1_1_2 context setting complete"
            )
        except Exception as err:
            print(
                "error while fetching section 1_1_2"
            )
            print(err)

        # get section 1.1.2 data
        try:
            secData_1_1_3 = fetchSection1_1_3Context(
                self.appDbConStr , startDt , endDt
            )
            reportContext.update(secData_1_1_3)
            print(
                "section 1_1_3 context setting complete"
            )
        except Exception as err:
            print(
                "error while fetching section 1_1_3")
        
        # get section 1.4.2 data
        try:
            secData_1_4_2 = fetchSection1_4_2Context(
                self.appDbConStr, startDt, endDt
            )
            reportContext.update(secData_1_4_2)
            print(
                "section 1_4_2 context setting complete"
            )
        except Exception as err:
            print(
                "error while fetching section 1_4_2"
            )
            print(err)

        # get section 1.1.2 data
        try:
            secData_1_1_4 = fetchSection1_1_4Context(
                self.appDbConStr , startDt , endDt
            )
            reportContext.update(secData_1_1_4)
            print(
                "section 1_1_4 context setting complete"
            )
        except Exception as err:
            print(
                "error while fetching section 1_1_4"
            )
            print(err)
        return reportContext

    def generateReportWithContext(self, reportContext: IReportCxt, tmplPath: str, dumpFolder: str) -> bool:
        """generate the report file at the desired dump folder location 
        based on the template file and report context object
        Args:
            reportContext (IReportCxt): report context object
            tmplPath (str): full file path of the template
            dumpFolder (str): folder path for dumping the generated report
        Returns:
            bool: True if process is success, else False
        """
        try:
            doc = DocxTemplate(tmplPath)
            # # signature Image
            # signatureImgPath = 'assets/signature.png'
            # signImg = InlineImage(doc, signatureImgPath)
            # reportContext['signature'] = signImg
            doc.render(reportContext)
            dumpFileName = 'Monthly_Report_{0}.docx'.format(
                reportContext['month_name'])
            dumpFileFullPath = os.path.join(dumpFolder, dumpFileName)
            doc.save(dumpFileFullPath)
        except Exception as err:
            print("error while saving monthly report from context for month ")
            print(err)
            return False
        return True

    def generateMonthlyReport(self, monthDt: dt.datetime, tmplPath: str, dumpFolder: str) -> bool:
        """generates and dumps weekly report for given dates at a desired location based on a template file
        Args:
            monthDt (dt.datetime): month date
            tmplPath (str): full file path of the template file
            dumpFolder (str): folder path where the generated reports are to be dumped
        Returns:
            bool: True if process is success, else False
        """
        reportCtxt = self.getReportContextObj(monthDt)
        isSuccess = self.generateReportWithContext(
            reportCtxt, tmplPath, dumpFolder)
        # convert report to pdf
        # convert(dumpFileFullPath, dumpFileFullPath.replace('.docx', '.pdf'))
        return isSuccess
