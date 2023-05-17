import pandas as pd
import math

from Event import MarketEvent
from Data.Data import DataHandler


class HistoricCSVDataHandler(DataHandler):
    """
    HistoricCSVDataHandler is designed to read CSV files for
    each requested symbol from disk and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface. Uses refactored bars of te 1min chart
    """

    def __init__(self, events, csv_dir, universe, timeframe_list, start_date, end_date):
        """
        Initialises the historic data handler by requesting
        the location of the CSV files and a list of symbols.

        It will be assumed that all files are of the form
        'symbol.csv', where symbol is a string in the list.

        Parameters:
        events - The Event Queue.
        csv_dir - Absolute directory path to the CSV files.
        symbol_list - A list of symbol strings.
        timeframe_list - A list of timeframe strings
        """
        self.events = events
        self.csv_dir = csv_dir
        self.universe = universe
        self.timeframe_list = timeframe_list
        self.start_date = start_date
        self.end_date = end_date

        self.timeframe_list_in_sec = {}

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.last_opentime = {s: {t: 0 for t in self.timeframe_list} for s in self.universe.symbol_list}

        self.continue_backtest = True

        self._open_convert_csv_files()

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.

        For this handler it will be assumed that the data is
        taken from Polygon. Thus its format will be respected.
        """
        comb_index = None
        for t in self.timeframe_list:
            self.timeframe_list_in_sec[t] = self.get_timeframe_in_sec(t)
            self.symbol_data[t] = {}
            self.latest_symbol_data[t] = {}
            for s in self.universe.symbol_list:
                # Load lowest timeframe data
                # Load the CSV file with no header information, indexed on date
                self.symbol_data[t][s] = pd.read_csv("{}\\{}\\{}.csv".format(self.csv_dir, self.timeframe_list[0], s))
                # Only use the bars that are after the start date and before the end date
                self.symbol_data[t][s] = self.symbol_data[t][s][self.symbol_data[t][s]["datetime"] >= self.start_date]
                self.symbol_data[t][s] = self.symbol_data[t][s][self.symbol_data[t][s]["datetime"] <= self.end_date]
                # Calculate the candle opentime
                self.symbol_data[t][s]["candle_opentime"] = self.symbol_data[t][s]["datetime"] - \
                    (self.symbol_data[t][s]["datetime"] % self.timeframe_list_in_sec[self.timeframe_list[0]])
                # Transform Data into lowest timeframe format
                dfgb = self.symbol_data[t][s].groupby("candle_opentime")

                df_hilf = pd.DataFrame()
                df_hilf["datetime"] = dfgb["datetime"].first()
                df_hilf["open"] = dfgb["open"].first()
                df_hilf["low"] = dfgb["low"].min()
                df_hilf["high"] = dfgb["high"].max()
                df_hilf["close"] = dfgb["close"].last()
                df_hilf["volume"] = dfgb["volume"].sum()
                df_hilf.reset_index()
                self.symbol_data[t][s] = df_hilf

                # Calculate new last candle in lowest timeframe
                #self.new_last_candle(t, s, self.timeframe_list[0])
                # Only use last candle
                #self.symbol_data[t][s] = self.symbol_data[t][s][self.symbol_data[t][s]["is last candle"] == True]
                # Calculate new last candle in current timeframe
                self.new_last_candle(t, s, t)

                self.symbol_data[t][s]["candle_closetime"] = self.symbol_data[t][s]["candle_opentime"] + \
                    self.timeframe_list_in_sec[t]
                try:
                    self.symbol_data[t][s] = self.symbol_data[t][s].set_index("Unnamed: 0")
                except KeyError:
                    print("No Column named Unnamed")

                # Combine the index to pad forward values
                if comb_index is None:
                    comb_index = self.symbol_data[t][s].index
                else:
                    comb_index.union(self.symbol_data[t][s].index)

                # Set the latest symbol_data to None
                self.latest_symbol_data[t][s] = []

        # Reindex the dataframes
        for t in self.timeframe_list:
            for s in self.universe.symbol_list:
                self.symbol_data[t][s] = self.symbol_data[t][s].reindex(index=comb_index, method='pad').iterrows()

    def _get_new_bar(self, symbol, timeframe):
        """
        Returns the latest bar from the data feed as a tuple of
        (symbol, datetime, open, low, high, close, volume, candle opentime, is new candle, is last candle).
        """
        for b in self.symbol_data[timeframe][symbol]:
            yield tuple([symbol, b[1][0], b[1][1], b[1][2], b[1][3], b[1][4], b[1][5], b[1][6], b[1][7], b[1][8]])

    def get_latest_bars(self, symbol, timeframe, n=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[timeframe][symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
        else:
            return bars_list[-n:]

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for s in self.universe.symbol_list:
            cur_time = 0
            for t in self.timeframe_list:
                try:
                    bar = self._get_new_bar(s, t).__next__()
                    if cur_time == 0:
                        cur_time = bar[7]
                    elif bar[8] is False:
                        old_bar = list(self.latest_symbol_data[t][s][-1])
                        bar = list(bar)
                        if bar[3] > old_bar[3]:
                            bar[3] = old_bar[3]
                        if bar[4] < old_bar[4]:
                            bar[4] = old_bar[4]
                        bar[6] += old_bar[6]
                        bar = tuple(bar)
                        self.latest_symbol_data[t][s][-1] = bar
                        bar = None
                except StopIteration:
                    print("No new bars")
                    print(t, s, len(self.latest_symbol_data[t][s]))
                    self.continue_backtest = False
                else:
                    if bar is not None and math.isnan(bar[7]) is False:
                        self.latest_symbol_data[t][s].append(bar)
        self.events.put(MarketEvent())

    def new_last_candle(self, t, s, t_sec):
        # Calculate the candle opentime
        self.symbol_data[t][s]["candle_opentime"] = self.symbol_data[t][s]["datetime"] - \
            (self.symbol_data[t][s]["datetime"] % self.timeframe_list_in_sec[t_sec])
        # calculate the is new candle column
        self.symbol_data[t][s]["is new candle"] = self.symbol_data[t][s]["candle_opentime"].diff()
        self.symbol_data[t][s].loc[self.symbol_data[t][s]["is new candle"] != 0, "is new candle"] = True
        self.symbol_data[t][s].loc[self.symbol_data[t][s]["is new candle"] == "NaN", "is new candle"] = True
        self.symbol_data[t][s].loc[self.symbol_data[t][s]["is new candle"] == 0, "is new candle"] = False
        # calculate the is last candle column
        self.symbol_data[t][s]["is last candle"] = self.symbol_data[t][s]["candle_opentime"] + \
            self.timeframe_list_in_sec[t_sec] - self.timeframe_list_in_sec[self.timeframe_list[0]]
        self.symbol_data[t][s].loc[self.symbol_data[t][s]["is last candle"] != self.symbol_data[t][s][
            "datetime"], "is last candle"] = False
        self.symbol_data[t][s].loc[self.symbol_data[t][s]["is last candle"] == self.symbol_data[t][s][
            "datetime"], "is last candle"] = True
