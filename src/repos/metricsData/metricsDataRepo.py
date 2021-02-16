from typing import List
import datetime as dt
from src.typeDefs.metricsDataRecord import IMetricsDataRecord
from src.repos.metricsData.getEntityMetricHourlyData import getEntityMetricHourlyData


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
