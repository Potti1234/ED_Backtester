import pandas as pd
import queue
import time
import os


class Event_Driven_Backtester:
    """
    This Event Driver Backtester backtests a strategy
    """

    def __init__(self, universe, bars, strategy, risk, port, commission, broker, events):
        """
        Initialises the Event-Driven Backtester.

        Parameters:
        universe = Symbols to trade
        bars = Historical Data
        strategy = Strategy to test
        risk = MoneyManagement
        port = Portfolio
        commission = Calculates the commissions
        broker = Execution
        events - list of events
        """
        self.universe = universe
        self.bars = bars
        self.strategy = strategy
        self.risk = risk
        self.port = port
        self.commission = commission
        self.broker = broker

        self.events = events

    def backtest(self):
        """
        Runs the Backtest
        """
        runtime = time.time()
        print(runtime)

        while 1:
            # Update the bars (specific backtest code, as opposed to live trading)
            if self.bars.continue_backtest is True:
                self.bars.update_bars()
            else:
                break

            # Handle the events
            while 1:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                else:
                    if event is not None:
                        if event.type == 'MARKET':
                            self.strategy.calculate_signals(event)
                            self.port.update_timeindex()

                        elif event.type == 'SIGNAL':
                            self.port.update_signal(event)

                        elif event.type == 'ORDER':
                            self.broker.execute_order(event)

                        elif event.type == 'FILL':
                            self.port.update_fill(event)

        runtime = time.time() - runtime
        print(runtime)

    def save_statistics(self, statistics_filename, indicator_list):
        """
        Saves statistics

        Parameters
        statistics_filename - The filename to store the data.
        indicator_list - list of indicators to save
        """
        # If directory does not exist create a new one
        if os.path.isdir(statistics_filename[:len(statistics_filename)-1]) is False:
            os.mkdir(statistics_filename[:len(statistics_filename)-1])
            # create the symbol directories and the Trades directory in them
            for s in self.universe.return_symbol_list():
                os.mkdir(statistics_filename + s)
                os.mkdir(statistics_filename + s + "\\Trades")

        self.port.create_equity_curve_dataframe()

        timeframe_list = self.bars.timeframe_list

        for s in self.universe.return_symbol_list():
            columns = ["datetime", "price", "size", "commission", "stop_loss", "take_profit", "OC", "symbol",
                       "BestTPPrice", "BestSLPrice"]
            for variable in self.strategy.variable_names:
                columns.append(variable)

            if os.path.isdir(statistics_filename + s) is False:
                os.mkdir(statistics_filename + s)
                os.mkdir(statistics_filename + s + "\\Trades")

            df = pd.DataFrame(self.port.Trades[s][timeframe_list[0]], columns=columns)
            df.to_csv(statistics_filename + s + "\\" + "Trades.csv")

            counter = 0
            for indicator in indicator_list:
                try:
                    df = pd.DataFrame(self.strategy.indicators.return_all_values(s, counter))
                    df["datetime"] = pd.DataFrame(self.strategy.indicators.return_all_values(s, counter, True))[0]
                    df.to_csv(statistics_filename + s + "\\" + indicator + ".csv")
                    counter += 1
                except KeyError:
                    counter += 1
                    continue

        self.port.get_equity_curve().to_csv(statistics_filename + "\\Return.csv")
