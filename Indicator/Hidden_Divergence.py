from Indicator.Indicator import Indicator


class Hidden_Divergence(Indicator):
    """
    Calculates the Hidden_Divergence
    """

    def __init__(self, timeframe, symbol, period, lower_barrier, upper_barrier, width, indicator):
        """
        Initialises the Hidden_Divergence indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        lower_barrier - The lower barrier of the indicator
        upper_barrier - The upper barrier of the indicator
        width - The amount of candles every step can take
        indicator - The indicator to spot the hidden divergence on
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.timeframe_sec = self.get_timeframe_in_sec(timeframe)
        self.lower_barrier = lower_barrier
        self.upper_barrier = upper_barrier
        self.width = width
        self.indicator = indicator
        self.indicator_values = [0]
        self.timestamp_values = []
        self.divergence = {}
        self.candle_locked = False

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        divergence_value = 0
        # Calculate indicator
        self.indicator.calculate_indicator(data, is_new_candle, is_last_candle)
        indicator_value = self.indicator.return_value(0)
        # Calculates the candle opentime
        candle_opentime = data[0][-1] - (data[0][-1] % self.timeframe_sec)
        # Set current divergence to start values
        self.divergence[str(candle_opentime)] = [indicator_value, data[4][-1], self.width, 0, "None"]
        # Checks if it is the last candle of the period
        if is_last_candle is True:
            # Checks if the indicator is below the lower barrier
            if indicator_value < self.lower_barrier:
                self.divergence[str(candle_opentime)][3] = 1
                self.divergence[str(candle_opentime)][4] = "Long"
            # Checks if the indicator is above the upper barrier
            elif indicator_value > self.upper_barrier:
                self.divergence[str(candle_opentime)][3] = 1
                self.divergence[str(candle_opentime)][4] = "Short"

            for key in list(self.divergence.items()):
                # if step is 0 or width is 0 delete the entry
                if self.divergence[key[0]][3] == 0 or self.divergence[key[0]][2] == 0:
                    del self.divergence[key[0]]
                # if step is 1 check if step 2 is completed
                elif self.divergence[key[0]][3] == 1:
                    if self.divergence[key[0]][4] == "Long":
                        if indicator_value > self.lower_barrier:
                            self.divergence[key[0]][3] = 2
                            self.divergence[key[0]][2] = self.width
                        else:
                            self.divergence[key[0]][2] -= 1
                    elif self.divergence[key[0]][4] == "Short":
                        if indicator_value < self.upper_barrier:
                            self.divergence[key[0]][3] = 2
                            self.divergence[key[0]][2] = self.width
                        else:
                            self.divergence[key[0]][2] -= 1
                # if step is 2 check if step 3 is completed
                elif self.divergence[key[0]][3] == 2:
                    if self.divergence[key[0]][4] == "Long":
                        if indicator_value < self.lower_barrier and indicator_value < self.divergence[key[0]][0]\
                                and data[4][-1] > self.divergence[key[0]][1]:
                            self.divergence[key[0]][3] = 3
                            self.divergence[key[0]][2] = self.width
                        else:
                            self.divergence[key[0]][2] -= 1
                    elif self.divergence[key[0]][4] == "Short":
                        if indicator_value > self.upper_barrier and indicator_value > self.divergence[key[0]][0] \
                                and data[4][-1] < self.divergence[key[0]][1]:
                            self.divergence[key[0]][3] = 3
                            self.divergence[key[0]][2] = self.width
                        else:
                            self.divergence[key[0]][2] -= 1
                # if step is 3 check if step 4 is completed
                elif self.divergence[key[0]][3] == 3:
                    if self.divergence[key[0]][4] == "Long":
                        if indicator_value > self.lower_barrier:
                            divergence_value = 1
                        else:
                            self.divergence[key[0]][2] -= 1
                    elif self.divergence[key[0]][4] == "Short":
                        if indicator_value < self.upper_barrier:
                            divergence_value = -1
                        else:
                            self.divergence[key[0]][2] -= 1

        if is_new_candle is True:
            self.indicator_values.append(divergence_value)
            self.timestamp_values.append(data[0][-1])
        elif self.indicator_values[-1] == 0:
            self.indicator_values[-1] = divergence_value
            self.timestamp_values[-1] = data[0][-1]

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

    @staticmethod
    def get_timeframe_in_sec(timeframe):
        """
        Convert the string timeframe int a int value
        Args:
            timeframe: the timeframe to convert

        Returns:
            int: seconds of the timeframe

        """
        seconds = 0
        if "minute" in timeframe:
            seconds = 60
            timeframe = timeframe.replace("minute", "")
        elif "hour" in timeframe:
            seconds = 60*60
            timeframe = timeframe.replace("hour", "")
        elif "day" in timeframe:
            seconds = 60*60*24
            timeframe = timeframe.replace("day", "")

        return seconds * int(timeframe)
