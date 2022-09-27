from ED_Backtester.Indicator.Indicator import Indicator

# from datetime import datetime


class VWAP(Indicator):
    """
    Calculates the VWAP
    """
    def __init__(self, timeframe, symbol, period):
        """
        Initialises the VWAP indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.indicator_values = []
        self.timestamp_values = []
        self.cum_vol = 0
        self.top = 0
        self.current_cum_vol = 0
        self.current_top = 0
        self.date = 0

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4] < 1):
            return

        low = data[2][-self.period:]
        high = data[3][-self.period:]
        close = data[4][-self.period:]
        volume = data[5][-self.period:]

        if is_new_candle is True:
            self.cum_vol = self.current_cum_vol
            self.top = self.current_top

        current_date = data[0][-1].date()
        if current_date != self.date:
            self.date = current_date
            self.cum_vol = 0
            self.top = 0

        self.current_top = self.top + (volume[-1] * (low[-1] + high[-1] + close[-1]) / 3)
        self.current_cum_vol = self.cum_vol + volume[-1]

        indicator_value = self.current_top / self.current_cum_vol

        if is_new_candle is True:
            self.indicator_values.append(indicator_value)
            self.timestamp_values.append(data[0][-1])
        elif is_new_candle is False:
            try:
                self.indicator_values[len(self.indicator_values) - 1] = indicator_value
                self.timestamp_values[-1] = data[0][-1]
            except IndexError:
                self.indicator_values.append(indicator_value)
                self.timestamp_values.append(data[0][-1])

    def return_value(self, shift, timestamp=False):
        """

        Args:
            shift: The amount of bars to go back
            timestamp: return timestamp

        Returns:
            The value of the indicator

        """
        if timestamp is False:
            try:
                return self.indicator_values[-shift - 1]
            except IndexError:
                return 50
        elif timestamp is True:
            try:
                return self.timestamp_values[-shift - 1]
            except IndexError:
                return 50

    def return_all_values(self, timestamp=False):
        if timestamp is False:
            return self.indicator_values
        elif timestamp is True:
            return self.timestamp_values
