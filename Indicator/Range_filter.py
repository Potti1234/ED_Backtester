from Indicator.Indicator import Indicator
from Indicator.SMA import SMA
from Indicator.EMA import EMA
from Indicator.Fractals import Fractals


class Range_filter(Indicator):
    """
    Calculates the Range Filter
    Trend increases for every ma value without a fractal in the opposite direction
    """

    def __init__(self, timeframe, symbol, period, fractal_period, mode):
        """
        Initialises the Range Filter indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the MA
        fractal_period - The period to calculate the fractals
        mode - Use MA or EMA
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.fractal_period = fractal_period
        self.indicator_values = []
        self.timestamp_values = []
        self.multiplier = 2 / (self.period + 1)
        if mode == "MA":
            self.MA = SMA(self.timeframe, self.symbol, self.period)
        elif mode == "EMA":
            self.MA = EMA(self.timeframe, self.symbol, self.period)
        self.Fractals = Fractals(self.timeframe, self.symbol, self.fractal_period)
        self.MA_values = [[], [], [], [], []]
        self.save_last_fractal = 0
        self.trend_start_price = 0

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return
        if is_last_candle is False:
            return

        self.MA.calculate_indicator(data, is_new_candle, is_last_candle)
        ma_value = self.MA.return_value(0)
        # Keep SMA values at the lenght of the defined period
        new_values = [data[0][-1], 0, ma_value, ma_value, 0]
        for i in range(5):
            if len(self.MA_values[i]) >= self.period:
                self.MA_values[i] = self.MA_values[i][1:]
            self.MA_values[i].append(new_values[i])

        self.Fractals.calculate_indicator(self.MA_values, is_last_candle, is_last_candle)
        last_fractal = self.Fractals.return_value(0)
        indicator_value = [0, 0]
        if last_fractal[1] == self.save_last_fractal:
            if last_fractal[0] == "min":
                indicator_value[0] = self.indicator_values[0][-1] + 1
            elif last_fractal[0] == "max":
                indicator_value[0] = self.indicator_values[0][-1] - 1
        else:
            self.save_last_fractal = last_fractal[1]
            if last_fractal[0] == "min":
                indicator_value[0] = 1
            elif last_fractal[0] == "max":
                indicator_value[0] = -1

        # If the trend changes save the trend start price
        if indicator_value[0] > 0 and self.return_value(0)[0] < 0:
            self.trend_start_price = data[4][-1]
        elif indicator_value[0] < 0 and self.return_value(0)[0] > 0:
            self.trend_start_price = data[4][-1]
        # Calculate the average steepness of the price during the trend
        if indicator_value[0] != 0:
            indicator_value[1] = (data[4][1] - self.trend_start_price) / indicator_value[0]

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
                return [0, 0]
        elif timestamp is True:
            try:
                return self.timestamp_values[-shift - 1]
            except IndexError:
                return [0, 0]

    def return_all_values(self, timestamp=False):
        if timestamp is False:
            return self.indicator_values
        elif timestamp is True:
            return self.timestamp_values
