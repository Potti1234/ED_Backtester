from ED_Backtester.Indicator.Indicator import Indicator
from ED_Backtester.Indicator.EMA import EMA


class MACD(Indicator):
    """
    Calculates the value of the MACD
    """
    def __init__(self, timeframe, symbol, period, fast_period, signal_period):
        """
        Initialises the MACD indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        """
        self.symbol = symbol
        self.period = period
        self.fast_period = fast_period
        self.signal_period = signal_period
        self.timeframe = timeframe
        self.indicator_values = []
        self.timestamp_values = []
        self.signal_data = [0] * 5
        self.signal_data[0] = [0] * signal_period
        self.signal_data[4] = [0] * signal_period
        self.EMA_slow = EMA(timeframe, symbol, period)
        self.EMA_fast = EMA(timeframe, symbol, fast_period)
        self.EMA_signal = EMA(timeframe, symbol, signal_period)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 2:
            return

        self.EMA_slow.calculate_indicator(data, is_new_candle, is_last_candle)
        self.EMA_fast.calculate_indicator(data, is_new_candle, is_last_candle)

        macd_value = self.EMA_fast.return_value(0) - self.EMA_slow.return_value(0)

        if is_new_candle is True:
            self.signal_data[4] = self.signal_data[4][1:len(self.signal_data[4])]
            self.signal_data[0] = self.signal_data[0][1:len(self.signal_data[0])]
            self.signal_data[4].append(macd_value)
            self.signal_data[0].append(data[0][-1])
        elif is_new_candle is False:
            self.signal_data[4][-1] = macd_value
            self.signal_data[0][-1] = data[0][-1]

        self.EMA_signal.calculate_indicator(self.signal_data, is_new_candle, is_last_candle)

        indicator_value = self.EMA_signal.return_value(0)

        if is_new_candle is True:
            self.indicator_values.append([macd_value, indicator_value])
            self.timestamp_values.append(data[0][-1])
        elif is_new_candle is False:
            try:
                self.indicator_values[-1] = [macd_value, indicator_value]
                self.timestamp_values[-1] = data[0][-1]
            except IndexError:
                self.indicator_values.append([macd_value, indicator_value])
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
