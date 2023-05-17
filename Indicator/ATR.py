from Indicator.Indicator import Indicator
from Indicator.SMA import SMA


class ATR(Indicator):
    """
    Calculates the ATR
    """

    def __init__(self, timeframe, symbol, period):
        """
        Initialises the ATR indicator.

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
        self.candle_size = [0] * 5
        self.candle_size[0] = [0] * period
        self.candle_size[4] = [0] * period
        self.SMA = SMA(self.timeframe, self.symbol, self.period)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        low = data[2][-self.period:]
        high = data[3][-self.period:]

        size = abs(low[-1] - high[-1])
        if is_new_candle is True:
            self.candle_size[4] = self.candle_size[4][1:len(self.candle_size[4])]
            self.candle_size[4].append(size)
            self.candle_size[0] = self.candle_size[0][1:len(self.candle_size[0])]
            self.candle_size[0].append(data[0][-1])
        else:
            self.candle_size[4][-1] = size
            self.candle_size[0][-1] = data[0][-1]

        self.SMA.calculate_indicator(self.candle_size, is_new_candle, is_last_candle)
        indicator_value = self.SMA.return_value(0)

        if is_new_candle is True:
            self.indicator_values.append(indicator_value)
            self.timestamp_values.append((data[0][-1]))
        else:
            try:
                self.indicator_values[-1] = indicator_value
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
