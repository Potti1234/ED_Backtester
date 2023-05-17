from Indicator.Indicator import Indicator
from Indicator.MajorSwingLevels import MajorSwingLevels
from Indicator.EMA import EMA


class TrendFilter(Indicator):
    """
    Calculates the direction of the trend
    """
    def __init__(self, timeframe, symbol, period, mode, macd_filter=False, macd_settings=None, atr_filter=False, atr_settings=None):
        """
        Initialises the Trendfilter indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        mode - The mode to calculate the trend can be EMA or MSL
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.mode = mode
        self.indicator_values = []
        self.timestamp_values = []
        if self.mode == "MSL":
            self.MSL = MajorSwingLevels(timeframe, symbol, period, macd_filter, macd_settings, atr_filter, atr_settings)
            self.last_MSL_Level = 0
        elif self.mode == "EMA":
            self.EMA = EMA(timeframe, symbol, period)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        close = data[4][-self.period:]

        indicator_value = 0

        if self.mode == "EMA":
            self.EMA.calculate_indicator(data, is_new_candle, is_last_candle)
            ema_value = self.EMA.return_value(0)

            # Check the trend direction
            if close[-1] > ema_value:
                if self.return_value(1) < 0:
                    indicator_value = 1
                else:
                    indicator_value = self.return_value(1) + 1
            elif close[-1] < ema_value:
                if self.return_value(1) > 0:
                    indicator_value = -1
                else:
                    indicator_value = self.return_value(1) - 1

        elif self.mode == "MSL":
            self.MSL.calculate_indicator(data, is_new_candle, is_last_candle)

            same_value = True
            while same_value:
                prev_msl_value = self.MSL.return_value(2+abs(indicator_value))
                msl_value = self.MSL.return_value(0+abs(indicator_value))
                if msl_value > prev_msl_value:
                    if indicator_value < 0:
                        same_value = False
                    else:
                        indicator_value += 1
                elif msl_value < prev_msl_value:
                    if indicator_value > 0:
                        same_value = False
                    else:
                        indicator_value -= 1
                else:
                    same_value = False

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
