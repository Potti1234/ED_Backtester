from Event import SignalEvent
from Strategy.Strategy import Strategy

from Indicator.Main_Indicator import MainIndicator


class MSLStrategy(Strategy):
    """
    This strategy is used to test MSL capabilities
    Open trade at every MSL level with tp at positive break and SL at negative break
    """

    def __init__(self, events, bars):
        """
        Initialises the MSLReversal strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events
        self.indicators = MainIndicator(events, bars, [["MajorSwingLevels", self.bars.timeframe_list[1], 5, False,
                                                        [12, 26, 9], True, 14],
                                                       ["TrendFilter", self.bars.timeframe_list[1], 5, "MSL", False,
                                                        [12, 26, 9], True, 14],
                                                       ["ATR", self.bars.timeframe_list[0], 14],
                                                       ["EMA", self.bars.timeframe_list[0], 200],
                                                       ["Range_Filter", self.bars.timeframe_list[0], 25, 5, "MA"],
                                                       ["Range_Filter", self.bars.timeframe_list[0], 50, 5, "MA"],
                                                       ["Range_Filter", self.bars.timeframe_list[0], 75, 5, "MA"],
                                                       ["Range_Filter", self.bars.timeframe_list[0], 100, 5, "MA"],
                                                       ["Range_Filter", self.bars.timeframe_list[0], 200, 5, "MA"]])
        self.MSL = [0, 0, 0, 0]
        self.TrendFilter = 0
        self.last_MSL = {k: 0 for k in self.bars.universe.symbol_list}
        self.ATR = {k: 0 for k in self.bars.universe.symbol_list}
        self.Range_Filter = {k: [0, 0, 0, 0, 0] for k in self.bars.universe.symbol_list}

        self.in_zone = {k: [0, 0] for k in self.bars.universe.symbol_list}
        self.in_MSL = {k: 0 for k in self.bars.universe.symbol_list}

        self.entry_MSL = {k: 0 for k in self.bars.universe.symbol_list}

        self.variable_names = ["MSLRetracement", "MSLBreakout", "Trend", "TimeinZone", "NewMSLTime", "Range_Filter25", "Range_Filter50", "Range_Filter75", "Range_Filter100", "Range_Filter200"]

    def calculate_signals(self, event):
        """
        For the MSLReversal Strategy we long when there is a higher low and
        a higher high and a pullback to the higher low, we short when there
        is a lower low and a lower high and a pullback to the lower low

        Parameters
        event - A MarketEvent object.
        """
        if event.type == 'MARKET':
            self.indicators.calculate_indicator()
            for s in self.bars.universe.symbol_list:
                bars = self.bars.get_latest_bars(s, self.bars.timeframe_list[0], n=1)
                if bars is not None and bars != []:
                    # Is end of the candle
                    if bars[0][9] is True:
                        self.MSL[3] = self.indicators.return_value(0, s, 0)
                        self.MSL[2] = self.indicators.return_value(1, s, 0)
                        self.MSL[1] = self.indicators.return_value(2, s, 0)
                        self.MSL[0] = self.indicators.return_value(3, s, 0)

                        self.TrendFilter = self.indicators.return_value(0, s, 1)

                        self.Range_Filter[s][0] = self.indicators.return_value(0, s, 4)[0]
                        self.Range_Filter[s][1] = self.indicators.return_value(0, s, 5)[0]
                        self.Range_Filter[s][2] = self.indicators.return_value(0, s, 6)[0]
                        self.Range_Filter[s][3] = self.indicators.return_value(0, s, 7)[0]
                        self.Range_Filter[s][4] = self.indicators.return_value(0, s, 8)[0]

                        if self.last_MSL[s] != self.MSL[3]:
                            # calculate ATR
                            time = self.indicators.return_value(0, s, 0, True) - \
                                   self.indicators.return_value(2, s, 0, True)
                            self.last_MSL[s] = self.MSL[3]
                            try:
                                self.ATR[s] = self.indicators.return_value(int(time/900), s, 2)
                            except TypeError:
                                print("No ATR for this value")

                            # Set MSL entry in zone value
                            self.in_MSL[s] = 1

                        else:
                            # Increase entry in zone value
                            self.in_MSL[s] += 1

                        if self.entry_MSL[s] == self.MSL[3]:
                            continue

                        # MSL must be there for at least 3 bars on 4H = 48 on 15M
                        # if self.in_MSL[s] < 48:
                        #    return

                        # Check for trailing#
                        """
                        if self.entry_MSL[s] != self.MSL[3]:
                            signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'SHORT',
                                                 self.MSL[3], None)
                            self.events.put(signal)
                            self.entry_MSL[s] = self.MSL[3]
                        """

                        # Check for long orders
                        # Higher Low Higher High
                        if self.TrendFilter > 2:
                            if self.MSL[-1] < self.MSL[-2]:
                                continue
                            stop_loss = self.MSL[-2]
                            take_profit = self.MSL[-1]
                            #stop_loss = self.MSL[-1]
                            #take_profit = bars[0][5] - abs(bars[0][5] - zone_low) * 6

                            variables = [(self.MSL[3] - bars[0][5]) / (self.MSL[3] - self.MSL[2]),
                                         (self.MSL[3] - self.MSL[2]) / (self.MSL[1] - self.MSL[2]),
                                         self.TrendFilter, self.in_zone[s][0], self.in_MSL[s], self.Range_Filter[s][0],
                                         self.Range_Filter[s][1], self.Range_Filter[s][2], self.Range_Filter[s][3],
                                         self.Range_Filter[s][4]]

                            signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'LONG',
                                                 stop_loss, take_profit, parameters=variables)
                            self.events.put(signal)
                            self.entry_MSL[s] = self.MSL[3]
                        # Check for short orders
                        # Lower Low Lower High
                        if self.TrendFilter < -2:
                            if self.MSL[-1] > self.MSL[-2]:
                                continue
                            stop_loss = self.MSL[-2]
                            take_profit = self.MSL[-1]
                            #stop_loss = self.MSL[-1]
                            #take_profit = bars[0][5] + abs(bars[0][5] - zone_high) * 6

                            variables = [(bars[0][5] - self.MSL[3]) / (self.MSL[2] - self.MSL[3]),
                                         (self.MSL[2] - self.MSL[3]) / (self.MSL[2] - self.MSL[1]),
                                         self.TrendFilter, self.in_zone[s][0], self.in_MSL[s], self.Range_Filter[s][0],
                                         self.Range_Filter[s][1], self.Range_Filter[s][2], self.Range_Filter[s][3],
                                         self.Range_Filter[s][4]]

                            signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'SHORT',
                                                 stop_loss, take_profit, parameters=variables)
                            self.events.put(signal)
                            self.entry_MSL[s] = self.MSL[3]