from typing import List
import datetime as dt
from src.typeDefs.metricsDataRecord import IMetricsDataRecord, IFreqMetricsDataRecord, IReservoirDataRecord , IOutageDataRecord
from src.typeDefs.soFarHighestDataRecord import ISoFarHighestDataRecord
from src.typeDefs.voltDataRecord import IVoltDataRecord
from src.typeDefs.rawFreqRecord import IRawFreqRecord
from src.repos.metricsData.getEntityMetricHourlyData import getEntityMetricHourlyData
from src.repos.metricsData.getEntityMetricDailyData import getEntityMetricDailyData
from src.repos.metricsData.getAllEntityMetricMonthlyData import getAllEntityMetricMonthlyData
from src.repos.metricsData.getFreqDailyData import getFreqDailyData
from src.repos.metricsData.getDailyVoltDataByLevel import getDailyVoltDataByLevel
from src.repos.metricsData.getSoFarHighestAllEntityData import getSoFarHighestAllEntityData
from src.repos.metricsData.insertSoFarHighest import insertSoFarHighest
from src.repos.metricsData.getRawFreq import getRawFreq
from src.repos.metricsData.getReservoirDailyData import getReservoirDailyData
from src.repos.metricsData.getGenerationLinesDailyData import getGenerationLinesDailyData
from src.repos.metricsData.getOutageDailyData import getOutageData
from src.repos.metricsData.getEntityREDataHourly import getEntityREHourlyData
from src.repos.metricsData.readRRASData import getRRASData
from src.repos.metricsData.getReservoirMonthlyData import getReservoirMonthlyData


class MetricsDataRepo():
    """Repository class for entity metrics data
    """
    appDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string
        """
        self.appDbConnStr = dbConStr

    def getEntityMetricHourlyData(self, entityName: str, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getEntityMetricHourlyData(appDbConnStr=self.appDbConnStr, entityName=entityName, metricName=metricName, startDt=startDt, endDt=endDt)

    def getEntityMetricDailyData(self, entityName: str, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getEntityMetricDailyData(appDbConnStr=self.appDbConnStr, entityName=entityName, metricName=metricName, startDt=startDt, endDt=endDt)

    def getAllEntityMetricMonthlyData(self, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getAllEntityMetricMonthlyData(appDbConnStr=self.appDbConnStr, metricName=metricName, startDt=startDt, endDt=endDt)

    def getDailyVoltDataByLevel(self, voltLvl: int, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IVoltDataRecord]:
        return getDailyVoltDataByLevel(appDbConnStr=self.appDbConnStr, lvl=voltLvl, metricName=metricName, startDt=startDt, endDt=endDt)

    def getFreqDailyData(self, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IFreqMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getFreqDailyData(appDbConnStr=self.appDbConnStr, metricName=metricName, startDt=startDt, endDt=endDt)

    def getSoFarHighestAllEntityData(self, metricName: str, report_month: dt.datetime) -> List[ISoFarHighestDataRecord]:
        """
        Gives all constituents so far highest data from so far highest table
        """
        return getSoFarHighestAllEntityData(appDbConnStr=self.appDbConnStr, metricName=metricName, report_month=report_month)

    def insertSoFarHighest(self, constituent: str, metricName: str, report_month: dt.datetime, data_value: float, data_time: dt.datetime) -> bool:
        """Update So Far Highest Table if Metric value for current month is greater than 
            previous month metric value

        Args:
            constituent (str): [description]
            metricName (str): [description]
            report_month (dt.datetime): [description]
            data_value (float): [description]
            data_time (dt.datetime): [description]

        Returns:
            bool: True if updates successfully
        """
        return insertSoFarHighest(appDbConnStr=self.appDbConnStr, constituent=constituent, metricName=metricName, report_month=report_month, data_value=data_value, data_time=data_time)

    def getRawFreq(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IRawFreqRecord]:
        return getRawFreq(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt)

    def getReservoirDailyData(self, entityName: str, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IReservoirDataRecord]:
        """fetches an entity metrics time series data from the app db
        Returns:
            bool: returns true if process is ok
        """
        return getReservoirDailyData(appDbConnStr=self.appDbConnStr, entityName=entityName, metricName=metricName, startDt=startDt, endDt=endDt)

    def getGenerationLinesDailyData(self, entityName: str, generatorName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getGenerationLinesDailyData(appDbConnStr=self.appDbConnStr, entityName=entityName, generatorName=generatorName, startDt=startDt, endDt=endDt)

    def getOutageData(self, shutdownType: str,  startDt: dt.datetime, endDt: dt.datetime) -> List[IOutageDataRecord]:
        """fetches type of outage data from the app db
        """
        return getOutageData(appDbConnStr=self.appDbConnStr,shutdownType=shutdownType , startDt = startDt , endDt = endDt)
    
    def getEntityREHourlyData(self , entity:str , startDt: dt.datetime, endDt: dt.datetime):
        return getEntityREHourlyData(appDbConnStr=self.appDbConnStr , entityName = entity , startDt = startDt , endDt = endDt)

    def getRRASData(self , filePath:str , startDt:dt.datetime ,  endDt:dt.datetime):
        return getRRASData(filePath , startDt , endDt)
    
    def getReservoirMonthlyData(self, startDt: dt.datetime, endDt: dt.datetime) -> List[IReservoirDataRecord]:
        """fetches an entity metrics time series data from the app db
        Returns:
            bool: returns true if process is ok
        """
        return getReservoirMonthlyData(appDbConnStr=self.appDbConnStr, startDt=startDt, endDt=endDt)