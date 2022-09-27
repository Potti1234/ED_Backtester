from ED_Backtester.Indicator.create_indicator import create_indicator


class MainIndicator:
    """
    The Main Indicator file used to calculate all the Indicators
    """
    def __init__(self, events, bars, indicator_list):
        """
        Initialises the Main indicator.

        Parameters:
        bars - The DataHandler object that provides bar information
        indicator_list - The list with indicators to calculate [name,timeframe,period,parameters]
        """
        self.bars = bars
        self.events = events
        self.indicator_list = indicator_list
        self.timeframe_list = []
        self.save_periods = [1] * 6  # datetime, open, low, high, close, volume
        self.Indicators = []
        for indicator in self.indicator_list:
            self.Indicators.append({})
            # Save Timeframes
            self.timeframe_list.append(indicator[1])

            for symbol in self.bars.universe.symbol_list:
                self.Indicators[-1][symbol] = create_indicator(self, indicator)
        # Get rid of duplicate timeframes
        self.timeframe_list = list(dict.fromkeys(self.timeframe_list))

        # for datetime save the most amount of candles
        self.save_periods[0] = max(self.save_periods)
        # Create empty list for every symbol and timeframe containing the max stored candles
        self.data = {}
        for symbol in self.bars.universe.symbol_list:
            self.data[symbol] = {}
            for timeframe in self.timeframe_list:
                self.data[symbol][timeframe] = []
                for i in range(6):
                    save = [0]*self.save_periods[i]
                    self.data[symbol][timeframe].append(save)

    def set_save_periods(self, period, Open=False, Low=False, High=False, Close=False, Volume=False):
        # open
        if Open is True:
            if self.save_periods[1] < period:
                self.save_periods[1] = period
        # low
        if Low is True:
            if self.save_periods[2] < period:
                self.save_periods[2] = period
        # high
        if High is True:
            if self.save_periods[3] < period:
                self.save_periods[3] = period
        # close
        if Close is True:
            if self.save_periods[4] < period:
                self.save_periods[4] = period
        # volume
        if Volume is True:
            if self.save_periods[5] < period:
                self.save_periods[5] = period

    def calculate_indicator(self):
        for symbol in self.bars.universe.symbol_list:
            new_last_candle = {}
            for timeframe in self.timeframe_list:
                new_bar = self.bars.get_latest_bars(symbol, timeframe, n=1)
                # If it is a new candle append it to the end of the df
                if new_bar != [] and new_bar is not None:
                    new_last_candle[timeframe] = [new_bar[0][8], new_bar[0][9]]
                    new_bar_index = [7, 2, 3, 4, 5, 6]
                    if new_bar[0][8] is True:
                        for i, nb in zip(list(range(6)), new_bar_index):
                            # Deletes first value
                            del self.data[symbol][timeframe][i][0]
                            # Appends new value
                            self.data[symbol][timeframe][i].append(new_bar[0][nb])
                    else:
                        for i, nb in zip(list(range(6)), new_bar_index):
                            self.data[symbol][timeframe][i][-1] = new_bar[0][nb]

            for indicator in self.Indicators:
                try:
                    timeframe = indicator[symbol].timeframe
                    indicator[symbol].calculate_indicator(self.data[symbol][timeframe], new_last_candle[timeframe][0],
                                                          new_last_candle[timeframe][1])
                except KeyError:
                    continue

    def return_value(self, shift, symbol, indicator_number, timestamp=False):
        """
        Args:
            shift: The amount of bars to go back
            symbol: The symbol to return the value
            indicator_number: The number of the Indicator to return the value
            timestamp: Return the timestamp

        Returns:
            The value of the indicator

        """
        try:
            return self.Indicators[indicator_number][symbol].return_value(shift, timestamp)
        except IndexError:
            return 50

    def return_all_values(self, symbol, indicator_number, timestamp=False):
        """

        Args:
            symbol: The symbol to return the value
            indicator_number: The number of the Indicator to return the value
            timestamp: Return the timestamp

        Returns:
            The value of the indicator

        """
        try:
            return self.Indicators[indicator_number][symbol].return_all_values(timestamp)
        except IndexError:
            return 50
