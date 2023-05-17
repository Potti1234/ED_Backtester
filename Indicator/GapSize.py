from Indicator.Indicator import Indicator
from is_premarket import is_premarket


class GapSize(Indicator):
    """
    Calculates the Gap size
    """
    def __init__(self, timeframe, symbol, period, open_time, close_time):
        """
        Initialises the Gap size indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculate the value
        open_time - Time the market opens in seconds
        close_time - Time the market closes in seconds
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.open_time = open_time
        self.close_time = close_time
        self.indicator_values = []
        self.timestamp_values = []

        self.open_price = 0
        self.close_price = 0

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        close = data[4][-self.period:]
        last_pm = is_premarket(data[0][-2], self.open_time, self.close_time)
        current_pm = is_premarket(data[0][-1], self.open_time, self.close_time)

        indicator_value = 0

        if current_pm is "PreMarket":
            self.open_price = close[-1]
        elif current_pm is "Market":
            if last_pm is "PreMarket":
                indicator_value = (self.open_price - self.close_price) / self.open_price
            self.close_price = close[-1]

        if indicator_value != 0:
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
                return 0
        elif timestamp is True:
            try:
                return self.timestamp_values[-shift - 1]
            except IndexError:
                return 0

    def return_all_values(self, timestamp=False):
        if timestamp is False:
            return self.indicator_values
        elif timestamp is True:
            return self.timestamp_values
