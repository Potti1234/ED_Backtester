from Event import SignalEvent
from Strategy.Strategy import Strategy

from Indicator.RSI import RSI


class RSIFutures(Strategy):
    """
    This strategy longs when the 5 minute RSI is lower then 20
    and shorts when the 5 minute RSI is greater than 80
    """

    def __init__(self, events, bars):
        """
        Initialises the RSI Futures strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events
        self.rsi5m = RSI(bars, "5minute", 4)
        self.rsi5mvalue = 50

        self.break_counter = {}
        self.direction = {}
        self.current_position = {}
        self.entry_price = {}
        self.last_candle_open_time = {}
        self.entry_price = {}
        for s in self.bars.universe.symbol_list:
            self.break_counter[s] = 0
            self.direction[s] = "NONE"
            self.current_position[s] = "NONE"
            self.last_candle_open_time[s] = 0
            self.entry_price[s] = 0

    def calculate_signals(self, event):
        """
        For the RSIFutures strategy we long when the 5 minute RSI is lower then 20
        and short when the 5 minute RSI is greater than 80

        Parameters
        event - A MarketEvent object.
        """
        if event.type == 'MARKET':
            self.rsi5m.calculate_indicator()
            for s in self.bars.universe.symbol_list:
                bars = self.bars.get_latest_bars(s, "5minute", n=1)
                self.rsi5mvalue = self.rsi5m.return_value(0, s)
                print(bars)
                # print(self.rsi5mvalue)
                if bars is not None and bars != []:
                    if self.last_candle_open_time[s] != bars[0][7]:
                        if self.rsi5mvalue >= 80:
                            # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                            signal = SignalEvent(bars[0][0], "5minute", bars[0][1], 'SHORT')
                            self.events.put(signal)
                        elif self.rsi5mvalue <= 20:
                            # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                            signal = SignalEvent(bars[0][0], "5minute", bars[0][1], 'LONG')
                            self.events.put(signal)

                    self.last_candle_open_time[s] = bars[0][7]
