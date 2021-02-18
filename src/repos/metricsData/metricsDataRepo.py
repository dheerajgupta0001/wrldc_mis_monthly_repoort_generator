from typing import List
import datetime as dt
from src.typeDefs.metricsDataRecord import IMetricsDataRecord
from typeDefs.soFarHighestDataRecord import ISoFarHighestDataRecord
from src.repos.metricsData.getEntityMetricHourlyData import getEntityMetricHourlyData
from src.repos.metricsData.getEntityMetricDailyData import getEntityMetricDailyData
from src.repos.metricsData.getAllEntityMetricMonthlyData import getAllEntityMetricMonthlyData
from src.repos.metricsData.getsoFarHighestMetricData import getSoFarHighestAllEntityData
from src.repos.metricsData.getAllEntityMetricHourlyData import getAllEntityMetricHourlyData
from src.repos.metricsData.updateSoFarHighest import updateSoFarHighest
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
    
    def getSoFarHighestAllEntityData(self, metricName: str, report_month:dt.datetime  ) -> List[ISoFarHighestDataRecord]:
        """
        Gives all constituents so far highest data from so far highest table
        """
        return getSoFarHighestAllEntityData(appDbConnStr=self.appDbConnStr, metricName = metricName, report_month = report_month )
    
    def getAllEntityMetricHourlyData(self, metricName: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IMetricsDataRecord]:
        """
        Gives all constituents so hourly data for a metric name for given startdt and enddt
        """
        return getAllEntityMetricHourlyData(appDbConnStr=self.appDbConnStr, metricName = metricName, startDt = startDt ,endDt = endDt )

    def updateSoFarHighestTable(self,constituent:str, metricName:str,report_month:dt.datetime,data_value:float,data_time:dt.datetime) -> bool:
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
        return updateSoFarHighest(appDbConnStr=self.appDbConnStr ,constituent = constituent , metricName = metricName, report_month = report_month , data_value = data_value , data_time = data_time) 