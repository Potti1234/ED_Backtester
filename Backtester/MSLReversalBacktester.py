from Universe.DynamicUniverse import DynamicUniverse
from Data.HistoricCSVDataHandler import HistoricCSVDataHandler
from Strategy.MSLReversal import MSLReversal
from Portfolio.NaivePortfolio import NaivePortfolio
from RiskManagement.FixedMoneyRiskManagement import FixedMoneyRiskManagement
from Commission.FTMO_Commission import FTMO_Commission
from Execution.SimulatedExecutionHandler import SimulatedExecutionHandler

from Backtester.Event_Driven_Backtester import Event_Driven_Backtester

import Symbol_lists as Symbol_lists
import queue
import time
from datetime import datetime


def main():
    indicator_list = ["MajorSwingLevels4H", "TrendFilter4H", "ATR15M"]

    statistics_filename = "D:\\AktienDaten\\Statistics\\MSLReversalReversed6TimesTP\\"

    csv_dir = "D:\\AktienDaten"
    symbol_list = Symbol_lists.return_forexpairs()
    # symbol_list = Symbol_lists.return_5majors()
    # symbol_list = ["EURUSD"]

    timeframe_list = ["15minute", "4hour"]
    start_date = "2019/01/01 00:00:00"
    # start_date = "2021/07/01 00:00:00"
    start_date = time.mktime(datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S').timetuple())
    end_date = "2023/01/01 00:00:00"
    end_date = time.mktime(datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S').timetuple())

    events = queue.Queue()

    universe = DynamicUniverse(symbol_list)
    universe.initialise_symbol_list("EUR")
    bars = HistoricCSVDataHandler(events, csv_dir, universe, timeframe_list, start_date, end_date)
    strategy = MSLReversal(events, bars)
    risk = FixedMoneyRiskManagement(bars, 1000)
    port = NaivePortfolio(bars, events, start_date, risk)
    commission = FTMO_Commission()
    broker = SimulatedExecutionHandler(events, commission)

    backtester = Event_Driven_Backtester(universe, bars, strategy, risk, port, commission, broker, events)

    backtester.backtest()

    backtester.save_statistics(statistics_filename, indicator_list)


if __name__ == "__main__":
    main()
