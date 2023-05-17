from Event import SignalEvent
from Strategy.Strategy import Strategy

from Indicator.Main_Indicator import MainIndicator


class MSLBreakout(Strategy):
    """
    This strategy checks if the last MSL is broken
    """

    def __init__(self, events, bars):
        """
        Initialises the MSLBreakout strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events
        self.indicators = MainIndicator(events, bars, [["MajorSwingLevels", self.bars.timeframe_list[0], 5, False,
                                                        [12, 26, 9], False, 14],
                                                       ["MajorSwingLevels", self.bars.timeframe_list[1], 5, False,
                                                        [12, 26, 9], False, 14],
                                                       ["TrendFilter", self.bars.timeframe_list[0], 5, "MSL", False,
                                                        [12, 26, 9], False, 14],
                                                       ["TrendFilter", self.bars.timeframe_list[1], 5, "MSL", False,
                                                        [12, 26, 9], False, 14],
                                                       ["ATR", self.bars.timeframe_list[0], 14],
                                                       ["MACD", self.bars.timeframe_list[0], 12, 26, 9]])
        self.MSL15m = [0, 0, 0, 0]
        self.MSL4h = [0, 0, 0, 0]
        self.TrendFilter15m = 0
        self.TrendFilter4h = 0
        self.MACD = 0

        self.last_MSL = {k: 0 for k in self.bars.universe.symbol_list}
        self.ATR = {k: 0 for k in self.bars.universe.symbol_list}

        self.in_zone = {k: [0, 0] for k in self.bars.universe.symbol_list}
        self.entry_MSL = {k: 0 for k in self.bars.universe.symbol_list}
        self.last_tf = {k: 0 for k in self.bars.universe.symbol_list}

        self.open_trade = {k: 0 for k in self.bars.universe.symbol_list}

        self.variable_names = ["MSLRetracement", "MSLBreakout", "Trend"]
        self.variables = {k: [] for k in self.bars.universe.symbol_list}

    def calculate_signals(self, event):
        """
        For the MSLBreakout Strategy we long when there is a higher low and
        a higher high on the 4H timeframe and a break of structure on the
        15 minute timeframe in the direction of the 4H timeframe

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
                        self.MSL15m[3] = self.indicators.return_value(0, s, 0)
                        self.MSL15m[2] = self.indicators.return_value(1, s, 0)
                        self.MSL15m[1] = self.indicators.return_value(2, s, 0)
                        self.MSL15m[0] = self.indicators.return_value(3, s, 0)

                        self.MSL4h[3] = self.indicators.return_value(0, s, 1)
                        self.MSL4h[2] = self.indicators.return_value(1, s, 1)
                        self.MSL4h[1] = self.indicators.return_value(2, s, 1)
                        self.MSL4h[0] = self.indicators.return_value(3, s, 1)

                        self.TrendFilter15m = self.indicators.return_value(0, s, 2)
                        self.TrendFilter4h = self.indicators.return_value(0, s, 3)

                        self.MACD = self.indicators.return_value(0, s, 5)

                        if self.entry_MSL[s] == self.MSL4h[3]:
                            continue

                        # New MSL Level
                        if self.in_zone[s][1] != self.MSL4h[1]:
                            self.in_zone[s] = [0, self.MSL4h[1]]
                        """
                        # Close trade if 15 min MSL break
                        if self.open_trade[s] > 0:
                            if self.TrendFilter15m < 0 and self.last_tf[s] > 0:
                                signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'EXIT')
                                self.events.put(signal)
                                self.open_trade[s] = 0
                        elif self.open_trade[s] < 0:
                            if self.TrendFilter15m > 0 and self.last_tf[s] < 0:
                                signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'EXIT')
                                self.events.put(signal)
                                self.open_trade[s] = 0
                        """

                        # Check for long orders
                        # Higher Low Higher High
                        if self.TrendFilter4h > 2:
                            # Below last broken MSL Level
                            if self.in_zone[s][0] > 0:
                                if self.TrendFilter15m > 0 and self.last_tf[s] < 0:
                                    stop_loss = self.MSL15m[-2]
                                    take_profit = bars[0][4] + (abs(bars[0][4] - self.MSL4h[-1]) * 0.8)

                                    retracement = (self.MSL4h[3] - bars[0][5]) / (self.MSL4h[3] - self.MSL4h[2])
                                    breakout = (self.MSL4h[3] - self.MSL4h[2]) / (self.MSL4h[1] - self.MSL4h[2])

                                    variables = [retracement, breakout, self.TrendFilter4h]

                                    signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'LONG',
                                                         stop_loss, take_profit, parameters=variables)
                                    self.events.put(signal)
                                    self.entry_MSL[s] = self.MSL4h[3]

                                    self.open_trade[s] = 1
                            elif bars[0][5] < self.MSL4h[1]:
                                self.in_zone[s][0] += 1

                        # Check for short orders
                        # Lower Low Lower High
                        if self.TrendFilter4h < -2:
                            # Above last broken MSL Level
                            if self.in_zone[s][0] > 0:
                                if self.TrendFilter15m < 0 and self.last_tf[s] > 0:
                                    stop_loss = self.MSL15m[-2]
                                    take_profit = bars[0][4] - (abs(bars[0][4] - self.MSL4h[-1]) * 0.8)

                                    retracement = (bars[0][5] - self.MSL4h[3]) / (self.MSL4h[2] - self.MSL4h[3])
                                    breakout = (self.MSL4h[2] - self.MSL4h[3]) / (self.MSL4h[2] - self.MSL4h[1])

                                    variables = [retracement, breakout, self.TrendFilter4h]

                                    signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'SHORT',
                                                         stop_loss, take_profit, parameters=variables)
                                    self.events.put(signal)
                                    self.entry_MSL[s] = self.MSL4h[3]

                                    self.open_trade[s] = -1
                            elif bars[0][5] > self.MSL4h[1]:
                                self.in_zone[s][0] += 1

                        if self.last_tf[s] != self.TrendFilter15m:
                            self.last_tf[s] = self.TrendFilter15m
