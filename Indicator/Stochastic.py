from Indicator.Indicator import Indicator
from Indicator.SMA import SMA


class Stochastic(Indicator):
    """
    Calculates the Stochastic
    """

    def __init__(self, timeframe, symbol, period, slow_period):
        """
        Initialises the Stochastic indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        """
        self.symbol = symbol
        self.period = period
        self.slow_period = slow_period
        self.timeframe = timeframe
        self.indicator_values = []
        self.timestamp_values = []
        self.stochastic = [0] * 5
        self.stochastic[0] = [0] * period
        self.stochastic[4] = [0] * period
        self.SMA = SMA(self.timeframe, self.symbol, self.slow_period)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        low = data[2][-self.period:]
        high = data[3][-self.period:]
        close = data[4][-self.period:]

        period_high = max(high)
        period_low = min(low)

        if period_high == period_low:
            return

        stochastic = ((close[-1] - period_low) / (period_high - period_low)) * 100

        if is_new_candle is True:
            self.stochastic[4] = self.stochastic[4][1:self.period+1]
            self.stochastic[4].append(stochastic)
            self.stochastic[0] = self.stochastic[0][1:self.period + 1]
            self.stochastic[0].append(data[0][-1])
        else:
            self.stochastic[4][-1] = stochastic
            self.stochastic[0][-1] = data[0][-1]
        self.SMA.calculate_indicator(self.stochastic, is_new_candle, is_last_candle)
        indicator_value = self.SMA.return_value(0)

        if is_new_candle is True:
            self.indicator_values.append([stochastic, indicator_value])
            self.timestamp_values.append(data[0][-1])
        else:
            try:
                self.indicator_values[-1] = [stochastic, indicator_value]
                self.timestamp_values[-1] = data[0][-1]
            except IndexError:
                self.indicator_values.append([stochastic, indicator_value])
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
