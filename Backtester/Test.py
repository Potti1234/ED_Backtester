from Universe.DynamicUniverse import DynamicUniverse 
from Data.HistoricCSVDataHandler import HistoricCSVDataHandler 
from Strategy.BuyAndHoldStrategy import BuyAndHoldStrategy 
from Portfolio.NaivePortfolio import NaivePortfolio 
from RiskManagement.FixedMoneyRiskManagement import FixedMoneyRiskManagement 
from Commission.FTMO_Commission import FTMO_Commission 
from Execution.SimulatedExecutionHandler import SimulatedExecutionHandler 
from Backtester.Event_Driven_Backtester import Event_Driven_Backtester 
import queue 
import time 
from datetime import datetime 


def main():
    statistics_filename = "D:\\AktienDaten\\Statistics\\Test\\" 
    csv_dir = "D:\\AktienDaten" 
    symbol_list = ["ES", "EURUSD"]
    timeframe_list = ["1 minute", "5 minutes", "15 minutes", "30 minutes", "1 hour", "4 hours", "1 day"]
    start_date = time.mktime(datetime.strptime("2000-01-01", '%Y/%m/%d').timetuple()) 
    end_date = time.mktime(datetime.strptime("2000-01-01", '%Y/%m/%d').timetuple()) 

    events = queue.Queue() 

    universe = DynamicUniverse(symbol_list) 
    universe.initialise_symbol_list("EUR") 
    bars = HistoricCSVDataHandler(events, csv_dir, universe, timeframe_list, start_date, end_date) 
    strategy = BuyAndHoldStrategy(events, bars) 
    risk = FixedMoneyRiskManagement(bars, 1000) 
    port = NaivePortfolio(bars, events, start_date, risk) 
    commission = FTMO_Commission() 
    broker = SimulatedExecutionHandler(events, commission) 

    indicator_list = [] 

    backtester = Event_Driven_Backtester(universe, bars, strategy, risk, port, commission, broker, events) 
    backtester.backtest() 
    backtester.save_statistics(statistics_filename, indicator_list) 


if __name__ == "__main__": 
    main() 
