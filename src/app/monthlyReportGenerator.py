import os
import datetime as dt
from src.typeDefs.appConfig import IAppConfig
from src.typeDefs.reportContext import IReportCxt
from typing import List
from docxtpl import DocxTemplate, InlineImage
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

        # get major generating unit outages
        try:
            reportContext['genOtgs'] = fetchMajorGenUnitOutages(
                self.appDbConStr, startDate, endDate)
            print(
                "major generating outages context setting complete")
        except Exception as err:
            print(
                "error while fetching major generating outages")
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
        monthDateLogString = dt.datetime.strftime(
            reportContext['monthDtObj'], '%Y-%m-%d')
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
            print("error while saving monthly report from context for month {0}".format(monthDateLogString))
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
