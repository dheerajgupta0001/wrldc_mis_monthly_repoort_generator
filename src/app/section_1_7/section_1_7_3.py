import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import pandas as pd
from src.app.section_1_7.section_1_7_2 import strip400
from src.app.section_1_7.section_1_7_1 import strip765
from src.typeDefs.section_1_7.section_1_7_3 import ISection_1_7_3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


def fetchSection1_7_3Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_7_3:
    fullMonthName = dt.datetime.strftime(startDt, "%b' %Y")
    mRepo = MetricsDataRepo(appDbConnStr)
    metrics = ["Max", "Min"]
    lvls = [400, 765]
    numPltsPerPage = 6
    numPages = 0
    for m in metrics:
        for l in lvls:
            voltData = mRepo.getDailyVoltDataByLevel(l, m, startDt, endDt)
            voltDf = pd.DataFrame(voltData)
            voltDf["data_val"] = pd.to_numeric(
                voltDf["data_val"], errors='coerce')
            voltDf = voltDf.pivot(index="data_time", columns="entity_name",
                                        values="data_val")
            if l == 400:
                voltDf.columns = [strip400(x) for x in voltDf.columns]
            elif l == 765:
                voltDf.columns = [strip765(x) for x in voltDf.columns]
            lowThresh = 300 if l == 400 else 650
            voltDf[voltDf < lowThresh] = np.nan
            numStations = voltDf.shape[1]
            pageStartStnInd = 0
            while pageStartStnInd < numStations:
                pageEndStnInd = pageStartStnInd + numPltsPerPage
                if pageEndStnInd >= numStations:
                    pageEndStnInd = numStations-1
                # create a plotting area and get the figure, axes handle in return
                fig, ax = plt.subplots(figsize=(7.5, 4.5))
                pltTitle = "{0}. Voltage Profile during the month of {1} - {2} kV S/S".format(
                    m, fullMonthName, l)
                # set plot title
                ax.set_title(pltTitle)
                # set x and y labels
                ax.set_xlabel('Date')
                ax.set_ylabel('kV')
                # enable y axis grid lines
                ax.yaxis.grid(True)
                for stnIter in range(pageStartStnInd, pageEndStnInd+1):
                    stnName = voltDf.columns[stnIter]
                    la, = ax.plot(
                        voltDf.index.values, voltDf[stnName].values, linestyle='solid', marker='.')
                    la.set_label(stnName)
                # set x axis locator as day of month
                ax.set_xlim((startDt, endDt), auto=True)
                ax.xaxis.set_major_locator(mdates.DayLocator())
                # set x axis formatter as month name
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
                # enable legends
                ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
                          ncol=numPltsPerPage, mode="expand", borderaxespad=0.)
                fig.subplots_adjust(bottom=0.2, left=0.07, right=0.99)
                fig.savefig('assets/section_1_7_3_{0}.png'.format(numPages))
                numPages += 1
                pageStartStnInd = pageEndStnInd + 1
    sectionData: ISection_1_7_3 = {'num_plts_sec_1_7_3': numPages}
    return sectionData
