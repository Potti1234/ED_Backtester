from Event import SignalEvent
from Strategy.Strategy import Strategy

from datetime import datetime


class EdwardFutures(Strategy):
    """
    This trading strategy is described in the Trading_Rules.txt document
    """

    def __init__(self, events, bars):
        """
        Initialises the Edward Futures strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        # self.timeframe_list = ["1minute", "5minute"]
        self.timeframe_list = ["5minute"]
        self.events = events
        self.same_color = {}
        self.break_counter = {}
        self.direction = {}
        self.current_position = {}
        self.entry_price = {}
        self.last_candle_open_time = {}
        self.entry_price = {}
        for s in self.bars.universe.symbol_list:
            self.same_color[s] = {}
            self.break_counter[s] = {}
            self.direction[s] = {}
            self.current_position[s] = {}
            self.last_candle_open_time[s] = {}
            self.entry_price[s] = {}
            for t in self.timeframe_list:
                self.same_color[s][t] = 0
                self.break_counter[s][t] = 0
                self.direction[s][t] = "NONE"
                self.current_position[s][t] = "NONE"
                self.last_candle_open_time[s][t] = 0
                self.entry_price[s][t] = 0

    def calculate_signals(self, event):
        """
        This trading strategy is described in the Trading_Rules.txt document

        Parameters
        event - A MarketEvent object.
        """
        if event.type == 'MARKET':
            for s in self.bars.universe.symbol_list:
                for t in self.timeframe_list:
                    bars1m = self.bars.get_latest_bars(s, t, n=3)
                    if bars1m is not None and len(bars1m) == 3:
                        # print(bars1m)
                        dt = datetime.fromtimestamp(bars1m[2][1])
                        hour = dt.hour
                        minute = dt.minute
                        if (hour == 15 and minute > 30) or (hour == 16):
                            if self.last_candle_open_time[s][t] != bars1m[2][7]:
                                # If a pattern is detected every bar the break counter
                                # gets reduced by 1 till it reaches 0
                                if self.break_counter[s][t] > 0:
                                    self.break_counter[s][t] -= 1
                                elif self.break_counter[s][t] == 0:
                                    self.break_counter[s][t] = 0
                                    self.direction[s][t] = "NONE"
                                    self.entry_price[s][t] = 0
                                # The Size of the current bar is calculated
                                bar_size = bars1m[1][5] - bars1m[1][2]
                                # Checks if the Current bar is Bullish
                                if bar_size > 0:
                                    # If there are 3 or more bars in the same direction
                                    # and the current bar reverses a entry is possible
                                    if self.same_color[s][t] <= -3:
                                        self.same_color[s][t] = 1
                                        self.break_counter[s][t] = 4
                                        self.direction[s][t] = "SHORT"
                                        self.entry_price[s][t] = bars1m[1][3]
                                    # If the current bar reverses the color streak gets reset
                                    elif self.same_color[s][t] < 0:
                                        self.same_color[s][t] = 1
                                    # If the current bar goes to the same direction
                                    # as the previous the streak gets increased by 1
                                    else:
                                        self.same_color[s][t] += 1
                                # Checks if the Current bar is Bullish
                                elif bar_size < 0:
                                    # If there are 3 or more bars in the same direction
                                    # and the current bar reverses a entry is possible
                                    if self.same_color[s][t] >= 3:
                                        self.same_color[s][t] = -1
                                        self.break_counter[s][t] = 4
                                        self.direction[s][t] = "LONG"
                                        self.entry_price[s][t] = bars1m[1][4]
                                    # If the current bar reverses the color streak gets reset
                                    elif self.same_color[s][t] > 0:
                                        self.same_color[s][t] = -1
                                    # If the current bar goes to the same direction
                                    # as the previous the streak gets increased by 1
                                    else:
                                        self.same_color[s][t] -= 1
                                # If the Current bar goes into no direction the streak gets set to 0
                                else:
                                    self.same_color[s][t] = 0

                                # Exit a position
                                if self.current_position[s][t] == "SHORT":
                                    # 2 opposite direction candles
                                    if self.same_color[s][t] >= 2:
                                        print("Exit 1")
                                        # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                        self.current_position[s][t] = "NONE"
                                        signal = SignalEvent(bars1m[0][0], t, bars1m[2][1], "EXIT")
                                        self.events.put(signal)
                                    # opposite direction candle overtakes the previous candle
                                    elif bars1m[0][2] < bars1m[1][5]:
                                        if bar_size > 0:
                                            print("Exit 2")
                                            # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                            self.current_position[s][t] = "NONE"
                                            signal = SignalEvent(bars1m[0][0], t, bars1m[2][1], "EXIT")
                                            self.events.put(signal)
                                elif self.current_position[s][t] == "LONG":
                                    # 2 opposite direction candles
                                    if self.same_color[s][t] <= -2:
                                        print("Exit 1")
                                        # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                        self.current_position[s][t] = "NONE"
                                        signal = SignalEvent(bars1m[0][0], t, bars1m[2][1], "EXIT")
                                        self.events.put(signal)
                                    # opposite direction candle overtakes the previous candle
                                    elif bars1m[0][2] > bars1m[1][5]:
                                        if bar_size < 0:
                                            print("Exit 2")
                                            # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                            self.current_position[s][t] = "NONE"
                                            signal = SignalEvent(bars1m[0][0], t, bars1m[2][1], "EXIT")
                                            self.events.put(signal)

                            # If a short entry is possible it checks if the current price
                            # is lower than the low of the pullback bar
                            if self.direction[s][t] == "SHORT":
                                if bars1m[2][5] < self.entry_price[s][t]:
                                    # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                    signal = SignalEvent(bars1m[0][0], t, bars1m[2][1], self.direction[s][t])
                                    self.same_color[s][t] = 0
                                    self.current_position[s][t] = "SHORT"
                                    self.direction[s][t] = "NONE"
                                    self.events.put(signal)
                            # If a long entry is possible it checks if the current price
                            # is higher than the high of the pullback bar
                            elif self.direction[s][t] == "LONG":
                                if bars1m[2][5] > self.entry_price[s][t]:
                                    # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                    signal = SignalEvent(bars1m[0][0], t, bars1m[2][1], self.direction[s][t])
                                    self.same_color[s][t] = 0
                                    self.current_position[s][t] = "LONG"
                                    self.direction[s][t] = "NONE"
                                    self.events.put(signal)

                            self.last_candle_open_time[s][t] = bars1m[2][7]

                        # If the current time is not within the trading time
                        # it resets the variables to the base value and exits the position
                        else:
                            self.same_color[s][t] = 0
                            self.break_counter[s][t] = 0
                            self.direction[s][t] = "NONE"
                            self.current_position[s][t] = "NONE"
                            self.last_candle_open_time[s][t] = bars1m[2][7]
                            self.entry_price[s][t] = 0
                            # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                            self.current_position[s][t] = "NONE"
                            signal = SignalEvent(bars1m[0][0], t, bars1m[2][1], "EXIT")
                            self.events.put(signal)
