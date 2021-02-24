import unittest
from src.config.appConfig import loadJsonConfig
from src.repos.metricsData.metricsDataRepo import MetricsDataRepo
import datetime as dt


class TestMetricsDataRepo(unittest.TestCase):
    def setUp(self):
        self.jsonConf = loadJsonConfig()

    def test_getEntityMetricHourlyData(self) -> None:
        """tests the function that gets hourly data of entity metric
        """
        appDbConnStr = self.jsonConf['appDbConnStr']
        mRepo = MetricsDataRepo(appDbConnStr)
        startDt = dt.datetime(2020, 1, 1)
        endDt = dt.datetime(2020, 1, 10)
        samples = mRepo.getEntityMetricHourlyData(
            "wr", "Demand(MW)", startDt, endDt)
        self.assertFalse(len(samples) == 0)

    def test_getDailyVoltDataByLevel(self) -> None:
        """tests the function that gets hourly data of entity metric
        """
        appDbConnStr = self.jsonConf['appDbConnStr']
        mRepo = MetricsDataRepo(appDbConnStr)
        startDt = dt.datetime(2020, 1, 1)
        endDt = dt.datetime(2020, 1, 10)
        samples = mRepo.getDailyVoltDataByLevel(
            765, "%Time >420 or 800", startDt, endDt)
        self.assertFalse(len(samples) == 0)

    def test_getSoFarHighestAllEntityData(self) -> None:
        """tests the function that gets hourly data of entity metric
        """
        appDbConnStr = self.jsonConf['appDbConnStr']
        mRepo = MetricsDataRepo(appDbConnStr)
        startDt = dt.datetime(2020, 12, 1)
        samples = mRepo.getSoFarHighestAllEntityData(
            "soFarHighestRequirement", startDt)
        self.assertFalse(len(samples) == 0)

    def test_getRawFreq(self) -> None:
        """tests the function that gets raw frequency data
        """
        appDbConnStr = self.jsonConf['appDbConnStr']
        mRepo = MetricsDataRepo(appDbConnStr)
        startDt = dt.datetime(2021, 2, 1)
        samples = mRepo.getRawFreq(startDt, startDt)
        self.assertFalse(len(samples) == 0)
