from ED_Backtester.Universe.Dynamic_Universe import DynamicUniverse
from ED_Backtester.Data.HistoricCSVDataHandler1min import HistoricCSVDataHandler
from ED_Backtester.Strategy.Edward_Futures import EdwardFutures
from ED_Backtester.Portfolio.NaivePortfolio import NaivePortfolio
from ED_Backtester.RiskManagement.FixedMoneyRiskManagement import FixedMoneyRiskManagement
from ED_Backtester.Commission.IB_Commission import IB_Commission
from ED_Backtester.Execution.SimulatedExecutionHandler import SimulatedExecutionHandler

from ED_Backtester.Backtester.Event_Driven_Backtester import Event_Driven_Backtester

import queue
import time
from datetime import datetime


def main():
    indicator_list = []

    statistics_filename = "D:\\AktienDaten\\Statistics\\EdwardFutures\\"

    csv_dir = "D:\\AktienDaten"
    symbol_list = ["ES"]

    timeframe_list = ["1minute", "5minutes"]
    #start_date = "2019/01/01 00:00:00"
    start_date = "2021/07/01 00:00:00"
    start_date = time.mktime(datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S').timetuple())
    end_date = "2022/01/01 00:00:00"
    end_date = time.mktime(datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S').timetuple())

    events = queue.Queue()

    universe = DynamicUniverse(symbol_list)
    bars = HistoricCSVDataHandler(events, csv_dir, universe, timeframe_list, start_date, end_date)
    strategy = EdwardFutures(events, bars)
    risk = FixedMoneyRiskManagement(bars, 1000)
    port = NaivePortfolio(bars, events, start_date, risk)
    commission = IB_Commission()
    broker = SimulatedExecutionHandler(events, commission)

    backtester = Event_Driven_Backtester(universe, bars, strategy, risk, port, commission, broker, events)

    backtester.backtest()

    backtester.save_statistics(statistics_filename, indicator_list)


if __name__ == "__main__":
    main()
