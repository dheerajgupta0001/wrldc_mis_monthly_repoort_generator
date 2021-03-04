from src.typeDefs.section_1_1.section_1_1_3 import ISection_1_1_3
import datetime as dt
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
from src.utils.addMonths import addMonths
import pandas as pd
import math
import matplotlib.pyplot as plt
from src.utils.convertDtToDayNum import convertDtToDayNum
from src.typeDefs.section_1_12.section_1_12 import ISection_1_12


def fetchSection1_12Context(appDbConnStr: str, startDt: dt.datetime, endDt: dt.datetime) -> ISection_1_1_3:
    monthDtObj = dt.datetime(startDt.year, startDt.month, 1)
    month_name = dt.datetime.strftime(startDt, "%b %y")
    mRepo = MetricsDataRepo(appDbConnStr)
    width = 0.3
    numPages = 0
    # get WR Unrestricted demand hourly values for this month and prev yr month
    wrErActMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'EAST REGION_NET ACT (MU)', startDt, endDt)

    wrErSchMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'EAST REGION_NET SCH(MU)', startDt, endDt)
    if (len(wrErActMuVals) > 0) & (len(wrErSchMuVals) > 0):
        # create plot image for demands of prev yr, prev month, this month
        pltWrErActObjs = [{'Date': convertDtToDayNum(
            x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrErActMuVals]
        pltWrErSchObjs = [{'Date': convertDtToDayNum(
            x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrErSchMuVals]
        pltDataObjs = pltWrErActObjs + pltWrErSchObjs

        pltDataDf = pd.DataFrame(pltDataObjs)
        pltDataDf = pltDataDf.pivot(
            index='Date', columns='colName', values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataErDf = pltDataDf
        pltDataDf["Date"] = [math.floor(x) for x in pltDataDf["Date"]]

        # derive plot title
        pltTitle = 'WR - ER EXCHANGES FOR {0}'.format(month_name)

        # create a plotting area and get the figure, axes handle in return
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        # set plot title
        ax.set_title(pltTitle)
        # set x and y labels
        ax.set_xlabel('Date')
        ax.set_ylabel('MW')
        # plot data and get the line artist object in return
        plt.bar(pltDataDf['Date'] - width, pltDataDf['EAST REGION_NET ACT (MU)'],
                width=width, color='#bf4040', label='ACTUAL')

        plt.bar(pltDataDf['Date'], pltDataDf['EAST REGION_NET SCH(MU)'],
                width=width, color='#4d88ff', label='SCH')

        # ax.set_xlim((1, 31), auto=True)
        # enable y axis grid lines
        ax.yaxis.grid(True)
        # enable legends
        ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
                  ncol=3, mode="expand", borderaxespad=0.)
        fig.subplots_adjust(bottom=0.25, top=0.8)
        # plt.show()
        fig.savefig('assets/section_1_12_{0}.png'.format(numPages))
        numPages += 1

    # section 1_12_2

    wrNrActMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'NORTH REGION_NET ACT (MU)', startDt, endDt)

    wrNrSchMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'NORTH REGION_NET SCH(MU)', startDt, endDt)

    if (len(wrNrActMuVals) > 0) & (len(wrNrSchMuVals) > 0):
        # create plot image for demands of prev yr, prev month, this month
        pltWrNrActObjs = [{'Date': convertDtToDayNum(
            x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrNrActMuVals]
        pltWrNrSchObjs = [{'Date': convertDtToDayNum(
            x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrNrSchMuVals]
        pltDataObjs = pltWrNrActObjs + pltWrNrSchObjs

        pltDataDf = pd.DataFrame(pltDataObjs)
        pltDataDf = pltDataDf.pivot(
            index='Date', columns='colName', values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataNrDf = pltDataDf
        pltDataDf["Date"] = [math.floor(x) for x in pltDataDf["Date"]]

        # derive plot title
        pltTitle = 'WR - NR EXCHANGES FOR {0}'.format(month_name)

        # create a plotting area and get the figure, axes handle in return
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        # set plot title
        ax.set_title(pltTitle)
        # set x and y labels
        ax.set_xlabel('Date')
        ax.set_ylabel('Energy in Mus')
        # plot data and get the line artist object in return
        plt.bar(pltDataDf['Date'] - width, pltDataDf['NORTH REGION_NET ACT (MU)'], width=width, color='#bf4040',
                label='ACTUAL')

        plt.bar(pltDataDf['Date'], pltDataDf['NORTH REGION_NET SCH(MU)'],
                width=width, color='#4d88ff', label='SCH')

        # ax.set_xlim((1, 31), auto=True)
        # enable y axis grid lines
        ax.yaxis.grid(True)
        # enable legends
        ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
                  ncol=3, mode="expand", borderaxespad=0.)
        fig.subplots_adjust(bottom=0.25, top=0.8)
        # plt.show()
        fig.savefig('assets/section_1_12_{0}.png'.format(numPages))
        numPages += 1

    # section 1_12_3

    wrSrActMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'SOUTH REGION_NET ACT (MU)', startDt, endDt)

    wrSrSchMuVals = mRepo.getGenerationLinesDailyData(
        'ir_regionwise_sch_act', 'SOUTH REGION_NET SCH(MU)', startDt, endDt)

    if (len(wrSrActMuVals) > 0) & (len(wrSrActMuVals) > 0):
        # create plot image for demands of prev yr, prev month, this month
        pltWrSrActObjs = [{'Date': convertDtToDayNum(
            x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrSrActMuVals]
        pltWrSrSchObjs = [{'Date': convertDtToDayNum(
            x["time_stamp"]), 'colName': x["generator_tag"], 'val': x["data_value"]} for x in wrSrSchMuVals]
        pltDataObjs = pltWrSrActObjs + pltWrSrSchObjs

        pltDataDf = pd.DataFrame(pltDataObjs)
        pltDataDf = pltDataDf.pivot(
            index='Date', columns='colName', values='val')
        pltDataDf.reset_index(inplace=True)
        pltDataSrDf = pltDataDf
        pltDataDf["Date"] = [math.floor(x) for x in pltDataDf["Date"]]

        # derive plot title
        pltTitle = 'WR - SR EXCHANGES FOR {0}'.format(month_name)

        # create a plotting area and get the figure, axes handle in return
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        # set plot title
        ax.set_title(pltTitle)
        # set x and y labels
        ax.set_xlabel('Date')
        ax.set_ylabel('Energy in Mus')
        # plot data and get the line artist object in return
        plt.bar(pltDataDf['Date'] - width, pltDataDf['SOUTH REGION_NET ACT (MU)'], width=width, color='#bf4040',
                label='ACTUAL')

        plt.bar(pltDataDf['Date'], pltDataDf['SOUTH REGION_NET SCH(MU)'],
                width=width, color='#4d88ff', label='SCH')

        # ax.set_xlim((1, 31), auto=True)
        # enable y axis grid lines
        ax.yaxis.grid(True)
        # enable legends
        ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
                  ncol=3, mode="expand", borderaxespad=0.)
        fig.subplots_adjust(bottom=0.25, top=0.8)
        # plt.show()
        fig.savefig('assets/section_1_12_{0}.png'.format(numPages))
        numPages += 1

    # section 1_12_4
    pltDataDf = pd.DataFrame()
    if (len(wrSrActMuVals) > 0) & (len(wrErActMuVals) > 0) & (len(wrNrActMuVals) > 0):
        pltDataDf['Date'] = pltDataErDf['Date']
        pltDataDf['ACTUAL'] = pltDataErDf['EAST REGION_NET ACT (MU)'] + \
            pltDataNrDf['NORTH REGION_NET ACT (MU)'] + \
            pltDataSrDf['SOUTH REGION_NET ACT (MU)']

        if (len(wrErSchMuVals) > 0) & (len(wrNrSchMuVals) > 0) & (len(wrSrSchMuVals) > 0):
            pltDataDf['SCH'] = pltDataErDf['EAST REGION_NET SCH(MU)'] + \
                pltDataNrDf['NORTH REGION_NET SCH(MU)'] + \
                pltDataSrDf['SOUTH REGION_NET SCH(MU)']

            # derive plot title
            pltTitle = 'WR NET INTER REGIONAL EXCHANGES FOR {0}'.format(month_name)

            # create a plotting area and get the figure, axes handle in return
            fig, ax = plt.subplots(figsize=(7.5, 4.5))
            # set plot title
            ax.set_title(pltTitle)
            # set x and y labels
            ax.set_xlabel('Date')
            ax.set_ylabel('Energy in Mus')
            # plot data and get the line artist object in return
            plt.bar(pltDataDf['Date'] - width, pltDataDf['ACTUAL'], width=width, color='#bf4040',
                    label='ACTUAL')

            plt.bar(pltDataDf['Date'], pltDataDf['SCH'],
                    width=width, color='#4d88ff', label='SCH')

            # ax.set_xlim((1, 31), auto=True)
            # enable y axis grid lines
            ax.yaxis.grid(True)
            # enable legends
            ax.legend(bbox_to_anchor=(0.0, -0.3, 1, 0), loc='lower center',
                    ncol=3, mode="expand", borderaxespad=0.)
            fig.subplots_adjust(bottom=0.25, top=0.8)
            # plt.show()
            fig.savefig('assets/section_1_12_{0}.png'.format(numPages))
            numPages += 1
    sectionData: ISection_1_12 = {'num_plts_sec_inter_regional': numPages}
    return sectionData