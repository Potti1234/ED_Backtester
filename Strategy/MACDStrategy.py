from ED_Backtester.Event import SignalEvent
from ED_Backtester.Strategy.Strategy import Strategy

from ED_Backtester.Indicator.Main_Indicator import MainIndicator


class MACDStrategy(Strategy):
    """
    This strategy checks if there is a crossover on the MACD
    and the EMA agrees.
    """

    def __init__(self, events, bars):
        """
        Initialises the MACD strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events
        self.indicators = MainIndicator(events, bars, [["MACD", self.bars.timeframe_list[0], 26, 12, 9],
                                                       ["EMA", self.bars.timeframe_list[0], 200],
                                                       ["MajorSwingLevels", self.bars.timeframe_list[0], 5]])
        self.prev_MACD_value = [0, 0]
        self.MACD_value = [0, 0]
        self.EMA_value = 0

    def calculate_signals(self, event):
        """
        For the MACD strategy we long when there is a MACD crossover below 0
        and the EMA is above the price we short when there is a MACD crossover
        above 0 and the EMA is below the price

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
                        self.prev_MACD_value = self.indicators.return_value(1, s, 0)
                        self.MACD_value = self.indicators.return_value(0, s, 0)
                        self.EMA_value = self.indicators.return_value(0, s, 1)
                        # Check for long orders
                        # EMA below close
                        if self.EMA_value < bars[0][5]:
                            # MACD crossover
                            if self.prev_MACD_value[0] < self.prev_MACD_value[1] and \
                                    self.MACD_value[0] > self.MACD_value[1]:
                                if self.prev_MACD_value[0] < 0 and self.prev_MACD_value[1] < 0 and \
                                        self.MACD_value[0] < 0 and self.MACD_value[1] < 0:
                                    stop_loss = 0
                                    last_bars = self.bars.get_latest_bars(s, self.bars.timeframe_list[0], n=7)
                                    for bar in range(6, 1, -1):
                                        if last_bars[bar][3] < last_bars[bar - 1][3]:
                                            stop_loss = last_bars[bar][3]
                                        else:
                                            break
                                    # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                    if stop_loss != 0:
                                        take_profit = bars[0][5] + ((bars[0][5] - stop_loss) * 1.5)
                                        signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'LONG',
                                                             stop_loss, take_profit)
                                        self.events.put(signal)
                        # Check for short orders
                        # EMA above close
                        elif self.EMA_value > bars[0][5]:
                            # MACD crossover
                            if self.prev_MACD_value[0] > self.prev_MACD_value[1] and \
                                    self.MACD_value[0] < self.MACD_value[1]:
                                if self.prev_MACD_value[0] > 0 and self.prev_MACD_value[1] > 0 and \
                                        self.MACD_value[0] > 0 and self.MACD_value[1] > 0:
                                    stop_loss = 0
                                    last_bars = self.bars.get_latest_bars(s, self.bars.timeframe_list[0], n=7)
                                    for bar in range(6, 1, -1):
                                        if last_bars[bar][4] > last_bars[bar - 1][4]:
                                            stop_loss = last_bars[bar][4]
                                        else:
                                            break
                                    # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                    if stop_loss !=0:
                                        take_profit = bars[0][5] - ((stop_loss - bars[0][5]) * 1.5)
                                        signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'SHORT',
                                                             stop_loss, take_profit)
                                        self.events.put(signal)
