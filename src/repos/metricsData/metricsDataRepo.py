from typing import List
import datetime as dt
from src.typeDefs.metricsDataRecord import IMetricsDataRecord, IFreqMetricsDataRecord, IReservoirDataRecord
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
