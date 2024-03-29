import os, os.path
import pandas as pd
import requests,json

from Event import MarketEvent
from Data.Data import DataHandler


class PolygonLiveDataHandler(DataHandler):
    """
    PolygonLiveDataHandler recieves the Data from WebSockets and
    the REST API provided by polygon.io
    """

    def __init__(self, events, key, universe, timeframe_list):
        """
        Initialises the polygon live data handler by requesting
        the API key and a list of symbols.

        Parameters:
        events - The Event Queue.
        key - Polygon API Key.
        symbol_list - A list of symbol strings.
        """
        self.events = events
        self.key = key
        self.universe = universe
        self.timeframe_list = timeframe_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True

    def _open_convert_csv_files(self):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.

        For this handler it will be assumed that the data is
        taken from Polygon. Thus its format will be respected.
        """
        comb_index = None
        for s in self.universe.symbol_list:
            # Load the CSV file with no header information, indexed on date
            self.symbol_data[s] = pd.io.parsers.read_csv(
                                      os.path.join(self.csv_dir, '%s.csv' % s),
                                      header=0, index_col=0,
                                      names=['datetime', 'open', 'low', 'high', 'close', 'volume']
                                  )

            # Combine the index to pad forward values
            if comb_index is None:
                comb_index = self.symbol_data[s].index
            else:
                comb_index.union(self.symbol_data[s].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[s] = []

        # Reindex the dataframes
        for s in self.universe.symbol_list:
            self.symbol_data[s] = self.symbol_data[s].reindex(index=comb_index, method='pad').iterrows()

    def _get_new_bar(self, symbol):
        """
        Returns the latest bar from the data feed as a tuple of
        (symbol, datetime, open, low, high, close, volume).
        """
        for b in self.symbol_data[symbol]:
            yield tuple([symbol, b[1][0], b[1][1], b[1][2], b[1][3], b[1][4], b[1][5]])

    def get_latest_bars(self, symbol, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
        else:
            return bars_list[-N:]

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for s in self.universe.symbol_list:
            try:
                bar = self._get_new_bar(s).__next__()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.latest_symbol_data[s].append(bar)
        self.events.put(MarketEvent())

    def get_Aggregate_Price_Data(self):
        r = requests.get("https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={}".format(self.key))
        data = json.loads(r.content)
        return data["tickers"]
