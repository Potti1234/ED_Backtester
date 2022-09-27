from ED_Backtester.Event import SignalEvent
from ED_Backtester.Strategy.Strategy import Strategy

from ED_Backtester.Indicator.Main_Indicator import MainIndicator


class MSLPinbar(Strategy):
    """
    This strategy checks if there is a pullback to at least
    the previous structure level and enters at a Pinbar candle
    """

    def __init__(self, events, bars):
        """
        Initialises the MSLPinbar strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events
        self.indicators = MainIndicator(events, bars, [["MajorSwingLevels", self.bars.timeframe_list[0], 5],
                                                       ["MajorSwingLevels", self.bars.timeframe_list[1], 5],
                                                       ["ATR", self.bars.timeframe_list[0], 14],
                                                       ["Pinbar", self.bars.timeframe_list[0], 14, True],
                                                       ["EngulfingCandle", self.bars.timeframe_list[0], 3],
                                                       ["TrendFilter", self.bars.timeframe_list[0], 5, "MSL"],
                                                       ["TrendFilter", self.bars.timeframe_list[1], 5, "MSL"]])
        self.MSL = [0, 0, 0, 0]
        self.MSL4h = [0, 0, 0, 0]
        self.ATR = 0
        self.Pinbar = 0
        self.EngulfingCandle = 0
        self.Trendfilter = [0, 0]

        self.entry_MSL = {k: 0 for k in self.bars.universe.symbol_list}

        self.variable_names = []
        self.variables = {k: [] for k in self.bars.universe.symbol_list}

    def calculate_signals(self, event):
        """
        For the MSLPinbar Strategy we long when there is a higher low
        and a higher high and a pullback to the last high and a bullish pinbar,
        we short when there is a lower low and a lower
        high and a pullback to the last low and a bearish pinbar

        Parameters
        event - A MarketEvent object.
        """
        if event.type == 'MARKET':
            self.indicators.calculate_indicator()
            for s in self.bars.universe.symbol_list:
                bars = self.bars.get_latest_bars(s, self.bars.timeframe_list[0], n=1)
                # print(bars)
                if bars is not None and bars != []:
                    # Is end of the candle
                    if bars[0][9] is True:
                        self.MSL[3] = self.indicators.return_value(0, s, 0)
                        self.MSL[2] = self.indicators.return_value(1, s, 0)
                        self.MSL[1] = self.indicators.return_value(2, s, 0)
                        self.MSL[0] = self.indicators.return_value(3, s, 0)

                        self.MSL4h[3] = self.indicators.return_value(0, s, 1)
                        self.MSL4h[2] = self.indicators.return_value(1, s, 1)
                        self.MSL4h[1] = self.indicators.return_value(2, s, 1)
                        self.MSL4h[0] = self.indicators.return_value(3, s, 1)

                        self.ATR = self.indicators.return_value(0, s, 2)

                        self.Pinbar = self.indicators.return_value(0, s, 3)
                        self.EngulfingCandle = self.indicators.return_value(0, s, 4)

                        self.Trendfilter[0] = self.indicators.return_value(0, s, 5)
                        self.Trendfilter[1] = self.indicators.return_value(0, s, 6)

                        if self.entry_MSL[s] == self.MSL[3]:
                            continue

                        #"""
                        # Check for long orders
                        # Higher Low Higher High
                        if self.Trendfilter[0] <= 0:
                            if self.Trendfilter[1] <= 1:
                                continue
                            #if bars[0][3] >= self.MSL[-3]:
                             #   return
                            if self.Pinbar <= 0:# or self.EngulfingCandle != 1:
                                continue
                            stop_loss = bars[0][3]# - self.ATR
                            #stop_loss = self.MSL[-2]# - self.ATR
                            take_profit = self.MSL4h[-1]# - self.ATR
                            #RRR = (take_profit - bars[0][5]) / (bars[0][5] - stop_loss)
                            #if RRR <= 1:
                            #    continue
                            signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1],
                                                 'LONG', stop_loss, take_profit)
                            self.events.put(signal)
                            self.entry_MSL[s] = self.MSL[3]
                        # Check for short orders
                        # Lower Low Lower High
                        elif self.Trendfilter[0] >= 0:
                            if self.Trendfilter[1] >= -1:
                                continue
                            #if bars[0][4] <= self.MSL[-3]:
                             #   return
                            if self.Pinbar >= 0:# or self.EngulfingCandle != -1:
                                continue
                            stop_loss = bars[0][4]# + self.ATR
                            #stop_loss = self.MSL[-2]# + self.ATR
                            take_profit = self.MSL4h[-1]# + self.ATR
                            #RRR = (bars[0][5] - take_profit) / (stop_loss - bars[0][5])
                            #if RRR <= 1:
                            #    continue
                            signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1],
                                                 'SHORT', stop_loss, take_profit)
                            self.events.put(signal)
                            self.entry_MSL[s] = self.MSL[3]
                        #"""
                        """
                        # Check for long orders
                        # Higher Low Higher High
                        if self.Trendfilter[1] >= 2:
                            if self.Trendfilter[0] != 1:
                                continue
                            # if bars[0][5] >= self.MSL[-3]:
                            #    continue
                            #if self.Pinbar != 1:  # or self.EngulfingCandle != 1:
                            #    continue
                            stop_loss = self.MSL[-2]# - self.ATR
                            #take_profit = self.MSL4h[-1]# - self.ATR
                            take_profit = bars[0][5] + (bars[0][5] - stop_loss) * 1.5
                            # RRR = (take_profit - bars[0][5]) / (bars[0][5] - stop_loss)
                            # if RRR <= 2:
                            #    continue
                            signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1],
                                                 'LONG', stop_loss, take_profit)
                            self.events.put(signal)
                            self.entry_MSL[s] = self.MSL4h[3]
                        # Check for short orders
                        # Lower Low Lower High
                        elif self.Trendfilter[1] <= -2:
                            if self.Trendfilter[0] != -1:
                                continue
                            # if bars[0][5] <= self.MSL[-3]:
                            #    continue
                            #if self.Pinbar != -1:  # or self.EngulfingCandle != -1:
                            #    continue
                            stop_loss = self.MSL[-2]# + self.ATR
                            #take_profit = self.MSL4h[-1]# + self.ATR
                            take_profit = bars[0][5] - (stop_loss - bars[0][5]) * 1.5
                            # RRR = (bars[0][5] - take_profit) / (stop_loss - bars[0][5])
                            # if RRR <= 2:
                            #    continue
                            signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1],
                                                 'SHORT', stop_loss, take_profit)
                            self.events.put(signal)
                            self.entry_MSL[s] = self.MSL4h[3]
                        """
