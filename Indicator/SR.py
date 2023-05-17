from Indicator.Indicator import Indicator


class SupportandResistance(Indicator):
    """
    Calculates the Support and Resistance lines
    """
    def __init__(self, timeframe, symbol, period, time_to_keep):
        """
        Initialises the SR indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        time_to_keep - The time to keep a SR line in seconds
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.time_to_keep = time_to_keep
        self.indicator_values = []
        self.timestamp_values = []
        self.indicator_save_values = []
        self.indicator_values_timestamp = []
        self.counter_max = 0
        self.counter_min = 0
        self.range_max = [0] * period
        self.range_min = [0] * period

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        """
        Calculates the SR lines
        """
        if len(data[2] < 1):
            return

        low = data[2][-self.period:]
        high = data[3][-self.period:]

        if len(self.indicator_save_values) != 0 and self.indicator_values_timestamp[0] < data[0][-1] - self.time_to_keep:
            self.indicator_save_values = self.indicator_save_values[1:len(self.indicator_save_values) - 1]
            self.indicator_values_timestamp = self.indicator_values_timestamp[1:len(self.indicator_values_timestamp)-1]

        current_max = max(self.range_max, default=0)
        value_max = round(high[-1], 2)

        current_min = min(self.range_min, default=0)
        value_min = round(low[-1], 2)

        self.range_max = self.range_max[1:self.period-1]
        self.range_max.append(value_max)

        self.range_min = self.range_min[1:self.period-1]
        self.range_min.append(value_min)

        if current_max == max(self.range_max, default=0):
            self.counter_max += 1
        else:
            self.counter_max = 0
        if self.counter_max == int(self.period / 2):
            self.indicator_save_values.append(current_max)
            self.indicator_values_timestamp.append((data[0][-1]))

        if current_min == min(self.range_min, default=0):
            self.counter_min += 1
        else:
            self.counter_min = 0
        if self.counter_min == int(self.period / 2):
            self.indicator_save_values.append(current_min)
            self.indicator_values_timestamp.append((data[0][-1]))

        if is_new_candle is True:
            self.indicator_values.append(self.indicator_save_values[-1])
            self.timestamp_values.append(data[0][-1])
        elif is_new_candle is False:
            try:
                self.indicator_values[-1] = self.indicator_save_values[-1]
                self.timestamp_values[-1] = data[0][-1]
            except IndexError:
                self.indicator_values.append(self.indicator_save_values[-1])
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
