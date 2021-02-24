import os
import datetime as dt
from src.typeDefs.reportContext import IReportCxt
from typing import List
from docxtpl import DocxTemplate, InlineImage
from src.app.section_1_1.section_1_1_1 import fetchSection1_1_1Context
from src.app.section_1_1.section_1_1_2 import fetchSection1_1_2Context
from src.app.section_1_1.section_1_1_3 import fetchSection1_1_3Context
from src.app.section_1_1.section_1_1_4 import fetchSection1_1_4Context
from src.app.section_1_1.section_1_1_freq import fetchSection1_1_freq_Context
from src.app.section_1_1.section_1_1_volt import fetchSection1_1_voltContext
from src.app.section_1_1.section_1_1_hydro import fetchSection1_1_hydroContext
from src.app.section_1_1.section_1_1_wind_solar import fetchSection1_1_WindSolarContext
from src.app.section_1_3.section_1_3_a import fetchSection1_3_aContext
from src.app.section_1_4.section_1_4_2 import fetchSection1_4_2Context
from src.app.section_1_3.section_1_3_b import fetchSection1_3_bContext
from src.app.section_1_5.section_1_5_1 import fetchSection1_5_1Context
from src.app.section_1_5.section_1_5_2 import fetchSection1_5_2Context
from src.app.section_1_5.section_1_5_3 import fetchSection1_5_3Context
from src.app.section_1_6.section_1_6_1 import fetchSection1_6_1Context
from src.app.section_1_9.section_1_9 import fetchSection1_9Context
from src.app.section_reservoir.section_reservoir import fetchReservoirContext
from src.utils.addMonths import addMonths
from src.typeDefs.section_1_3.section_1_3_a import ISection_1_3_a
from src.typeDefs.section_1_3.section_1_3_b import ISection_1_3_b
# from docx2pdf import convert


class MonthlyReportGenerator:
    appDbConStr: str = ''

    sectionCtrls = {
        '1_1_1': True,
        '1_1_2': True,
        '1_1_3': True,
        '1_1_4': True,
        '1_1_freq': True,
        '1_1_volt': True,
        '1_1_hydro': True,
        '1_1_wind_solar': True,
        '1_4_2': True,
        '1_3_a': True,
        '1_3_b': True,
        '1_5_1': True,
        '1_5_2': True,
        '1_5_3': True,
        '1_6_1': True,
        '1_6_2': True,
        '1_9': True,
        'reservoir': True
    }

    def __init__(self, appDbConStr: str, secCtrls: dict = {}):
        self.appDbConStr = appDbConStr
        self.sectionCtrls.update(secCtrls)

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

        if self.sectionCtrls["reservoir"]:
            # get section reservoir data
            try:
                secData_reservoir = fetchReservoirContext(
                    self.appDbConStr, startDt, endDt)
                reportContext.update(secData_reservoir)
                print(
                    "section reservoir context setting complete")
            except Exception as err:
                print(
                    "error while fetching section reservoir")
                print(err)

        if self.sectionCtrls["1_1_1"]:
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

        if self.sectionCtrls["1_1_2"]:
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

        if self.sectionCtrls["1_1_3"]:
            # get section 1.1.2 data
            try:
                secData_1_1_3 = fetchSection1_1_3Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_3)
                print(
                    "section 1_1_3 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_3")

        if self.sectionCtrls["1_1_4"]:
            # get section 1.1.2 data
            try:
                secData_1_1_4 = fetchSection1_1_4Context(
                    self.appDbConStr, startDt, endDt
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

        # get section 1.1 volt data
        if self.sectionCtrls["1_1_volt"]:
            try:
                secData_1_1_volt = fetchSection1_1_voltContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_volt)
                print(
                    "section 1_1_volt context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_volt"
                )
                print(err)

        if self.sectionCtrls["1_1_freq"]:
            # get section 1.1.freq data
            try:
                secData_1_1_freq = fetchSection1_1_freq_Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_freq)
                print(
                    "section 1_1_freq context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_freq"
                )
                print(err)

        if self.sectionCtrls["1_1_hydro"]:
            # get section 1.1.hydro data
            try:
                secData_1_1_hydro = fetchSection1_1_hydroContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_hydro)
                print(
                    "section 1_1_hydro context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_hydro"
                )
                print(err)

        if self.sectionCtrls["1_1_wind_solar"]:
            # get section 1.1.wind_solar data
            try:
                secData_1_1_wind_solar = fetchSection1_1_WindSolarContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_1_wind_solar)
                print(
                    "section 1_1_wind_solar context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_1_wind_solar"
                )
                print(err)

        # get section 1.3.a data
        if self.sectionCtrls["1_3_a"]:
            try:
                secData_1_3_a: ISection_1_3_a = fetchSection1_3_aContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_3_a)
                print(
                    "section 1_3_a context setting complete"
                )
            except Exception as err:
                print("error while fetching section 1_3_a")
                print(err)

        # get section 1.3.b data
        if self.sectionCtrls['1_3_b']:
            try:
                secData_1_3_b: List[ISection_1_3_b] = fetchSection1_3_bContext(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_3_b)
                print('section_1_3_b context setting complete')
            except Exception as err:
                print("error while fetching section 1_3_b")
                print(err)

        if self.sectionCtrls["1_4_2"]:
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

        if self.sectionCtrls["1_5_1"]:
            # get section 1.5.1 data
            try:
                secData_1_5_1 = fetchSection1_5_1Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_5_1)
                print(
                    "section 1_5_1 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_5_1"
                )
                print(err)

        if self.sectionCtrls["1_5_2"]:
            # get section 1.5.2 data
            try:
                secData_1_5_2 = fetchSection1_5_2Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_5_2)
                print(
                    "section 1_5_2 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_5_2"
                )
                print(err)

        if self.sectionCtrls["1_5_3"]:
            # get section 1.5.3 data
            try:
                secData_1_5_3 = fetchSection1_5_3Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_5_3)
                print(
                    "section 1_5_3 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_5_3"
                )
                print(err)

        if self.sectionCtrls["1_6_1"]:
            # get section 1.6.1 data
            try:
                secData_1_6_1 = fetchSection1_6_1Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_6_1)
                print(
                    "section 1_6_1 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_6_1"
                )
                print(err)

        if self.sectionCtrls["1_9"]:
            # get section 1.6.1 data
            try:
                secData_1_9 = fetchSection1_9Context(
                    self.appDbConStr, startDt, endDt
                )
                reportContext.update(secData_1_9)
                print(
                    "section 1_9 context setting complete"
                )
            except Exception as err:
                print(
                    "error while fetching section 1_9"
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
            # populate section 1.4.2 plot image in word file
            if self.sectionCtrls["1_4_2"]:
                plot_1_4_2_path = 'assets/section_1_4_2.png'
                plot_1_4_2_img = InlineImage(doc, plot_1_4_2_path)
                reportContext['plot_1_4_2'] = plot_1_4_2_img

            # populate section 1.5.1 plot image in word file
            if self.sectionCtrls["1_5_1"]:
                plot_1_5_1_path = 'assets/section_1_5_1.png'
                plot_1_5_1_img = InlineImage(doc, plot_1_5_1_path)
                reportContext['plot_1_5_1'] = plot_1_5_1_img

            # populate section 1.5.2 plot image in word file
            if self.sectionCtrls["1_5_2"]:
                plot_1_5_2_path = 'assets/section_1_5_2.png'
                plot_1_5_2_img = InlineImage(doc, plot_1_5_2_path)
                reportContext['plot_1_5_2'] = plot_1_5_2_img

            # populate section 1.5.3 plot image in word file
            if self.sectionCtrls["1_5_3"]:
                plot_1_5_3_path = 'assets/section_1_5_3.png'
                plot_1_5_3_img = InlineImage(doc, plot_1_5_3_path)
                reportContext['plot_1_5_3'] = plot_1_5_3_img

            # populate section 1.5.3 plot image in word file
            if self.sectionCtrls["1_6_2"]:
                plot_1_6_2_path = 'assets/section_1_6_2.png'
                plot_1_6_2_img = InlineImage(doc, plot_1_6_2_path)
                reportContext['plot_1_6_2'] = plot_1_6_2_img

            # populate all reservoir section plot images in word file
            if self.sectionCtrls["reservoir"]:
                plot_reservoir_base_path = 'assets/reservoir_section'
                reportContext['reservoir_section'] = []
                for imgItr in range(reportContext['num_plts_sec_reservoir']):
                    imgPath = '{0}_{1}.png'.format(
                        plot_reservoir_base_path, imgItr)
                    img = InlineImage(doc, imgPath)
                    imgObj = {"img": img}
                    reportContext['reservoir_section'].append(imgObj)

            doc.render(reportContext)

            # derive document path and save
            dumpFileName = 'Monthly_Report_{0}.docx'.format(
                reportContext['full_month_name'])
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
