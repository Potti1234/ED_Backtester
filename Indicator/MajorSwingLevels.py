from Indicator.Indicator import Indicator
from Indicator.MACD import MACD
from Indicator.ATR import ATR


class MajorSwingLevels(Indicator):
    """
    Calculates the Major Swing Levels
    """
    def __init__(self, timeframe, symbol, period, macd_filter=False, macd_settings=None, atr_filter=False, atr_settings=None):
        """
        Initialises the Major Swing Levels indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.macd_filter = macd_filter
        self.atr_filter = atr_filter

        self.macd_value = [0, 0]
        if macd_filter is True:
            self.macd = MACD(self.timeframe, self.symbol, macd_settings[0], macd_settings[1], macd_settings[2])
        self.atr_value = 0
        if atr_filter is True:
            self.atr = ATR(self.timeframe, self.symbol, atr_settings)
        # swing low, swing high
        self.indicator_values = []
        self.timestamp_values = []

        self.broke_High_Low = [False, False]
        self.High_Low = "None"
        # High value High timestamp Low value Low timestamp
        self.High_Low_save = [[0, 0], [0, 0]]

        self.period_middle = int(self.period / 2 + 0.5)

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < self.period:
            return

        if self.macd_filter is True:
            self.macd.calculate_indicator(data, is_new_candle, is_last_candle)
            self.macd_value = self.macd.return_value(self.period_middle - 1)

        if self.atr_filter is True:
            self.atr.calculate_indicator(data, is_new_candle, is_last_candle)
            self.atr_value = self.atr.return_value(0)

        if is_last_candle is not True:
            return

        low = data[2][-self.period:]
        high = data[3][-self.period:]
        close = data[4][-self.period:]

        # Check for a swing low
        swing_low = 0
        current_min = min(low, default=0)
        if low[self.period_middle] == current_min:
            if self.macd_value[0] - self.macd_value[1] <= 0:
                swing_low = current_min
        # Check for a swing high
        swing_high = 0
        current_max = max(high, default=0)
        if high[self.period_middle] == current_max:
            if self.macd_value[0] - self.macd_value[1] >= 0:
                swing_high = current_max

        if self.High_Low == "High" and close[-1] - self.atr_value > self.indicator_values[-1]:
            self.broke_High_Low[0] = True
        elif self.High_Low == "Low" and close[-1] + self.atr_value < self.indicator_values[-1]:
            self.broke_High_Low[1] = True

        if swing_low == swing_high:
            return

        # First swing level
        if len(self.indicator_values) == 0:
            if swing_low != 0:
                self.append_value(data[0], swing_low, "Low")
            elif swing_high != 0:
                self.append_value(data[0], swing_high, "High")
        # Second swing level
        elif len(self.indicator_values) == 1:
            if swing_low != 0:
                if self.High_Low == "Low":
                    self.replace_value(data[0], swing_low)
                elif self.High_Low == "High":
                    self.append_value(data[0], swing_low, "Low")
            elif swing_high != 0:
                if self.High_Low == "High":
                    self.replace_value(data[0], swing_high)
                elif self.High_Low == "Low":
                    self.append_value(data[0], swing_high, "High")
        # Third+ swing level
        elif len(self.indicator_values) >= 2:
            if swing_low != 0:
                if self.High_Low == "Low" and swing_low < self.indicator_values[-1] and self.broke_High_Low[1] is True:
                    self.broke_High_Low[0] = False
                    if self.High_Low_save[0][0] == 0:
                        self.replace_value(data[0], swing_low)
                    else:
                        # Append high
                        self.append_value(int(self.High_Low_save[0][1]), self.High_Low_save[0][0], "Low")
                        self.High_Low_save = [[0, 0], [0, 0]]
                        # Append low
                        self.append_value(data[0], swing_low, "Low")
                elif self.High_Low == "High":
                    if swing_low < self.indicator_values[-2]:
                        self.High_Low_save = [[0, 0], [0, 0]]
                        self.append_value(data[0], swing_low, "Low")
                    elif self.High_Low_save[1][0] > swing_low or self.High_Low_save[1][0] == 0:
                        self.High_Low_save[1][0] = swing_low
                        self.High_Low_save[1][1] = data[0][-self.period_middle]
            elif swing_high != 0:
                if self.High_Low == "High" and swing_high > self.indicator_values[-1] and \
                        self.broke_High_Low[0] is True:
                    self.broke_High_Low[0] = False
                    if self.High_Low_save[1][0] == 0:
                        self.replace_value(data[0], swing_high)
                    else:
                        # Append low
                        self.append_value(int(self.High_Low_save[1][1]), self.High_Low_save[1][0], "High")
                        self.High_Low_save = [[0, 0], [0, 0]]
                        # Append high
                        self.append_value(data[0], swing_high, "High")
                elif self.High_Low == "Low":
                    if swing_high > self.indicator_values[-2]:
                        self.High_Low_save = [[0, 0], [0, 0]]
                        self.append_value(data[0], swing_high, "High")
                    elif self.High_Low_save[0][0] < swing_high or self.High_Low_save[0][0] == 0:
                        self.High_Low_save[0][0] = swing_high
                        self.High_Low_save[0][1] = data[0][-self.period_middle]

    def append_value(self, time, value, hl):
        if isinstance(time, int) is True:
            self.timestamp_values.append(time)
        else:
            self.timestamp_values.append(time[-self.period_middle])
        self.indicator_values.append(value)
        self.High_Low = hl

    def replace_value(self, time, value):
        self.timestamp_values[-1] = time[-self.period_middle]
        self.indicator_values[-1] = value

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
