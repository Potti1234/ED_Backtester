from ED_Backtester.Indicator.Indicator import Indicator
from ED_Backtester.Indicator.SMA import SMA


class EMA(Indicator):
    """
    Calculates the EMA
    """

    def __init__(self, timeframe, symbol, period):
        """
        Initialises the EMA indicator.

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
        self.multiplier = 2 / (self.period + 1)
        self.SMA = SMA(self.timeframe, self.symbol, self.period)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        close = data[4][-self.period:]

        # SMA if available data is lower than period or the first data
        if len(self.indicator_values) < self.period:
            self.SMA.calculate_indicator(data, is_new_candle, is_last_candle)
            indicator_value = self.SMA.return_value(0)

            if is_new_candle is True:
                self.indicator_values.append(indicator_value)
                self.timestamp_values.append(data[0][-1])
            elif is_new_candle is False:
                try:
                    self.indicator_values[-1] = indicator_value
                    self.timestamp_values[-1] = data[0][-1]
                except IndexError:
                    self.indicator_values.append(indicator_value)
                    self.timestamp_values.append(data[0][-1])
        # EMA calculation if there are enough values
        else:
            if is_new_candle is True:
                indicator_value = (close[-1] * self.multiplier) + (self.indicator_values[-1] * (1 - self.multiplier))
                self.indicator_values.append(indicator_value)
                self.timestamp_values.append(data[0][-1])
            elif is_new_candle is False:
                try:
                    indicator_value = (close[-1] * self.multiplier) + (self.indicator_values[-2] * (1 - self.multiplier))
                    self.indicator_values[len(self.indicator_values) - 1] = indicator_value
                    self.timestamp_values[-1] = data[0][-1]
                except IndexError:
                    indicator_value = (close[-1] * self.multiplier) + (
                                self.indicator_values[-1] * (1 - self.multiplier))
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
