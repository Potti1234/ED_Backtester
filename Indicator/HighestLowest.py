from Indicator.Indicator import Indicator


class HighestLowest(Indicator):
    """
    Calculates the Highest and Lowest value of the last N candles
    """
    def __init__(self, timeframe, symbol, period):
        """
        Initialises the Highest Lowest indicator.

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

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        low = data[2][-self.period:]
        high = data[3][-self.period:]

        indicator_value = [max(high), min(low)]

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
                return [50, 50]
        elif timestamp is True:
            try:
                return self.timestamp_values[-shift - 1]
            except IndexError:
                return [50, 50]

    def return_all_values(self, timestamp=False):
        if timestamp is False:
            return self.indicator_values
        elif timestamp is True:
            return self.timestamp_values
