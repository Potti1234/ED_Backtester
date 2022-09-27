from ED_Backtester.Indicator.Indicator import Indicator
from ED_Backtester.Indicator.ATR import ATR


class Pinbar(Indicator):
    """
    Finds pinbars on the chart
    """
    def __init__(self, timeframe, symbol, period, atr_filter):
        """
        Initialises the Pinbar indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        atr_filter - Use ATR to filter out small pinbars
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.atrfilter = atr_filter
        self.indicator_values = []
        self.timestamp_values = []
        if self.atrfilter is True:
            self.ATR = ATR(self.timeframe, self.symbol, self.period)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        Open = data[1][-self.period:]
        low = data[2][-self.period:]
        high = data[3][-self.period:]
        close = data[4][-self.period:]

        indicator_value = 0
        body_size = close[-1] - Open[-1]
        candle_size = high[-1] - low[-1]
        # red candle
        if body_size < 0:
            if (candle_size / 3) * 2 < high[-1] - Open[-1]:
                indicator_value = -2
            elif (candle_size / 3) * 2 < close[-1] - low[-1]:
                indicator_value = 1
        # green candle
        elif body_size > 0:
            if (candle_size / 3) * 2 < Open[-1] - low[-1]:
                indicator_value = 2
            elif (candle_size / 3) * 2 < high[-1] - close[-1]:
                indicator_value = -1

        if self.atrfilter is True:
            self.ATR.calculate_indicator(data, is_new_candle, is_last_candle)
            if candle_size < self.ATR.return_value(0):
                indicator_value = 0

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
