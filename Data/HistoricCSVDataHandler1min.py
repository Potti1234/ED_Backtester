import pandas as pd

from Event import MarketEvent
from Data.Data import DataHandler


class HistoricCSVDataHandler1min(DataHandler):
    """
    HistoricCSVDataHandler is designed to read CSV files for
    each requested symbol from disk and provide an interface
    to obtain the "latest" bar in a manner identical to a live
    trading interface.
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
                # Load the CSV file with no header information, indexed on date
                self.symbol_data[t][s] = pd.read_csv("{}\\{}\\{}.csv".format(self.csv_dir, t, s))
                # Only use the bars that are after the start date and before the end date
                self.symbol_data[t][s] = self.symbol_data[t][s][self.symbol_data[t][s]["datetime"] >= self.start_date]
                self.symbol_data[t][s] = self.symbol_data[t][s][self.symbol_data[t][s]["datetime"] <= self.end_date]
                # Calculate the candle opentime
                self.symbol_data[t][s]["candle_opentime"] = self.symbol_data[t][s]["datetime"] - \
                    (self.symbol_data[t][s]["datetime"] % self.timeframe_list_in_sec[t])
                # calculate the is new candle column
                self.symbol_data[t][s]["is new candle"] = self.symbol_data[t][s]["candle_opentime"].diff()
                self.symbol_data[t][s].loc[self.symbol_data[t][s]["is new candle"] != 0, "is new candle"] = True
                self.symbol_data[t][s].loc[self.symbol_data[t][s]["is new candle"] == "NaN", "is new candle"] = True
                self.symbol_data[t][s].loc[self.symbol_data[t][s]["is new candle"] == 0, "is new candle"] = False
                # calculate the is last candle column
                self.symbol_data[t][s]["is last candle"] = self.symbol_data[t][s]["candle_opentime"] + \
                    self.timeframe_list_in_sec[t] - 60
                self.symbol_data[t][s].loc[self.symbol_data[t][s]["is last candle"] != self.symbol_data[t][s][
                    "datetime"], "is last candle"] = False
                self.symbol_data[t][s].loc[self.symbol_data[t][s]["is last candle"] == self.symbol_data[t][s][
                    "datetime"], "is last candle"] = True

                try:
                    self.symbol_data[t][s] = self.symbol_data[t][s].set_index("Unnamed: 0")
                except KeyError:
                    continue

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
                print(t, len(self.symbol_data[t][s]))
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
        for t in self.timeframe_list:
            for s in self.universe.symbol_list:
                try:
                    bar = self._get_new_bar(s, t).__next__()
                except StopIteration:
                    print(t, s, len(self.latest_symbol_data[t][s]))
                    print("No new bars")
                    self.continue_backtest = False
                else:
                    if bar is not None:
                        if bar[8] is True:
                            self.latest_symbol_data[t][s].append(bar)
                        elif bar[8] is False:
                            try:
                                self.latest_symbol_data[t][s][len(self.latest_symbol_data[t][s]) - 1] = bar
                            except IndexError:
                                self.latest_symbol_data[t][s].append(bar)
        self.events.put(MarketEvent())

