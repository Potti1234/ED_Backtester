from Universe.DynamicUniverse import DynamicUniverse
from Data.HistoricCSVDataHandler1min import HistoricCSVDataHandler1min
from Strategy.MSLPinbar import MSLPinbar
from Portfolio.NaivePortfolio import NaivePortfolio
from RiskManagement.FixedMoneyRiskManagement import FixedMoneyRiskManagement
from Commission.IB_Commission import IB_Commission
from Execution.SimulatedExecutionHandler import SimulatedExecutionHandler

from Backtester.Event_Driven_Backtester import Event_Driven_Backtester

import Symbol_lists as Symbol_lists
import queue
import time
from datetime import datetime
import Constants


def main():
    indicator_list = ["MajorSwingLevel1H", "MajorSwingLevel4H", "ATR", "Pinbar", "EngulfingCandle", "TrendFilter1H", "TrendFilter4H"]

    statistics_filename = Constants.STATISTICS_DIRECTORY + "Test\\"

    csv_dir = Constants.DATA_DIRECTORY
    symbol_list = Symbol_lists.return_5majors()

    timeframe_list = ["30minute", "4hour"]
    start_date = "2019/01/01 00:00:00"
    #start_date = "2021/07/01 00:00:00"
    start_date = time.mktime(datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S').timetuple())
    end_date = "2022/01/01 00:00:00"
    end_date = time.mktime(datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S').timetuple())

    events = queue.Queue()

    universe = DynamicUniverse(symbol_list)
    bars = HistoricCSVDataHandler1min(events, csv_dir, universe, timeframe_list, start_date, end_date)
    strategy = MSLPinbar(events, bars)
    risk = FixedMoneyRiskManagement(bars, 1000)
    port = NaivePortfolio(bars, events, start_date, risk)
    commission = IB_Commission()
    broker = SimulatedExecutionHandler(events, commission)

    backtester = Event_Driven_Backtester(universe, bars, strategy, risk, port, commission, broker, events)

    backtester.backtest()

    backtester.save_statistics(statistics_filename, indicator_list)


if __name__ == "__main__":
    main()
