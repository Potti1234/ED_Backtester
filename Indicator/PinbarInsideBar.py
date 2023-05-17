from Indicator.Indicator import Indicator
from Indicator.Pinbar import Pinbar


class PinbarInsideBar(Indicator):
    """
    Calculates the Pinbar Inside Bar
    """

    def __init__(self, timeframe, symbol, period, atr_filter):
        """
        Initialises the Pinbar Inside Bar indicator.

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

        self.Pinbar = Pinbar(self.timeframe, self.symbol, self.period, self.atrfilter)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        low = data[2][-self.period:]
        high = data[3][-self.period:]

        self.Pinbar.calculate_indicator(data, is_new_candle, is_last_candle)
        pinbar_value = self.Pinbar.return_value(1)

        indicator_value = 0

        if high[-1] < high[-2] and low[-1] > low[-2]:
            indicator_value = pinbar_value

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
