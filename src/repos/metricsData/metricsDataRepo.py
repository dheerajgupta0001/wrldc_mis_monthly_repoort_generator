from typing import List
import datetime as dt
from src.typeDefs.metricsDataRecord import IMetricsDataRecord, IFreqMetricsDataRecord
from src.repos.metricsData.getEntityMetricHourlyData import getEntityMetricHourlyData
from src.repos.metricsData.getEntityMetricDailyData import getEntityMetricDailyData
from src.repos.metricsData.getAllEntityMetricMonthlyData import getAllEntityMetricMonthlyData
from src.repos.metricsData.getFreqDailyData import getFreqDailyData


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

    def getFreqDailyData(self, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IFreqMetricsDataRecord]:
        """inserts a entity metrics time series data into the app db
        Returns:
            bool: returns true if process is ok
        """
        return getFreqDailyData(appDbConnStr=self.appDbConnStr, metricName=metricName, startDt=startDt, endDt=endDt)
