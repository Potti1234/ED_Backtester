from Indicator.Indicator import Indicator
from Indicator.EMA import EMA


class RSI(Indicator):
    """
    Calculates the value of the RSI
    """
    def __init__(self, timeframe, symbol, period):
        """
        Initialises the RSI indicator.

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
        self.up = [0] * 5
        self.up[0] = [0] * period
        self.up[4] = [0] * period
        self.down = [0] * 5
        self.down[0] = [0] * period
        self.down[4] = [0] * period
        self.roll_up = EMA(timeframe, symbol, period)
        self.roll_down = EMA(timeframe, symbol, period)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 2:
            return

        close = data[4][-self.period:]

        delta = close[-1] - close[-2]
        if is_new_candle is True:
            self.up[4] = self.up[4][1:len(self.up[4])]
            self.up[0] = self.up[0][1:len(self.up[0])]
            self.down[4] = self.down[4][1:len(self.down[4])]
            self.down[0] = self.down[0][1:len(self.down[0])]
            if delta > 0:
                self.up[4].append(delta)
                self.up[0].append(data[0][-1])
                self.down[4].append(0)
                self.down[0].append(data[0][-1])
            else:
                self.up[4].append(0)
                self.up[0].append(data[0][-1])
                self.down[4].append(abs(delta))
                self.down[0].append(data[0][-1])
        elif is_new_candle is False:
            if delta > 0:
                self.up[4][-1] = delta
                self.up[0][-1] = data[0][-1]
                self.down[4][-1] = 0
                self.down[0][-1] = data[0][-1]
            else:
                self.up[4][-1] = 0
                self.up[0][-1] = data[0][-1]
                self.down[4][-1] = abs(delta)
                self.down[0][-1] = data[0][-1]

        self.roll_up.calculate_indicator(self.up, is_new_candle, is_last_candle)
        self.roll_down.calculate_indicator(self.down, is_new_candle, is_last_candle)

        try:
            rs = self.roll_up.return_value(0) / self.roll_down.return_value(0)
        except ZeroDivisionError:
            rs = 1
        indicator_value = 100 - 100 / (1 + rs)

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
