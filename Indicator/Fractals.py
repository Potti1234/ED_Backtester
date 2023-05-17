from Indicator.Indicator import Indicator


class Fractals(Indicator):
    """
    Calculates the Fractals
    """
    def __init__(self, timeframe, symbol, period):
        """
        Initialises the Fractals indicator.

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

        self.period_middle = int(self.period / 2 + 0.5)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[2]) < self.period:
            return
        if is_last_candle is not True:
            return
        low = data[2][-self.period:]
        high = data[3][-self.period:]

        # Check for a swing low
        current_min = min(low, default=0)
        if low[self.period_middle] == current_min:
            self.indicator_values.append(["min", current_min])
            self.timestamp_values.append(data[0][-1])
        # Check for a swing high
        current_max = max(high, default=0)
        if high[self.period_middle] == current_max:
            self.indicator_values.append(["max", current_max])
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
                return ["None", 0]
        elif timestamp is True:
            try:
                return self.timestamp_values[-shift - 1]
            except IndexError:
                return ["None", 0]

    def return_all_values(self, timestamp=False):
        if timestamp is False:
            return self.indicator_values
        elif timestamp is True:
            return self.timestamp_values
