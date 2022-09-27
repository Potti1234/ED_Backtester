from ED_Backtester.Event import SignalEvent
from ED_Backtester.Strategy.Strategy import Strategy

from ED_Backtester.Indicator.Main_Indicator import MainIndicator


class HD_RSI_Stochastic_EMA(Strategy):
    """
    This strategy checks if there is Hidden Divergence on the Price and RSI
    then enters if the Stochastic indicator gives a signal and the EMA agrees.
    """

    def __init__(self, events, bars):
        """
        Initialises the HD RSI Stochastic EMA strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events
        self.indicators = MainIndicator(events, bars, [["Hidden Divergence", self.bars.timeframe_list[0], 1, 50, 50, 10,
                                                        ["RSI", self.bars.timeframe_list[0], 14]],
                                                       ["Stochastic", self.bars.timeframe_list[0], 14, 3],
                                                       ["EMA", self.bars.timeframe_list[0], 200]])
        self.width = 10

        self.HD_value = 0
        self.prev_Stochastic_value = [0, 0]
        self.Stochastic_value = [0, 0]
        self.EMA_value = 0

        self.Hidden_Divergence = {}
        for s in self.bars.universe.symbol_list:
            # Signal, width, low/high
            self.Hidden_Divergence[s] = [0, self.width, 0]

    def calculate_signals(self, event):
        """
        For the RSIFutures strategy we long when the 5 minute RSI is lower then 20
        and short when the 5 minute RSI is greater than 80

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
                        self.HD_value = self.indicators.return_value(0, s, 0)
                        self.prev_Stochastic_value = self.indicators.return_value(1, s, 1)
                        self.Stochastic_value = self.indicators.return_value(0, s, 1)
                        self.EMA_value = self.indicators.return_value(0, s, 2)
                        # Check if there is Hidden Divergence
                        if self.HD_value == 1:
                            # Save the value with the high
                            self.Hidden_Divergence[s] = [self.HD_value, self.width, bars[0][3]]
                        elif self.HD_value == -1:
                            # Save the value with the low
                            self.Hidden_Divergence[s] = [self.HD_value, self.width, bars[0][4]]
                        else:
                            if self.Hidden_Divergence[s][0] == 1:
                                # If there is a new low
                                if self.Hidden_Divergence[s][2] < bars[0][3]:
                                    self.Hidden_Divergence[s][2] = bars[0][3]
                            elif self.Hidden_Divergence[s][0] == -1:
                                # if there is a new high
                                if self.Hidden_Divergence[s][2] > bars[0][4]:
                                    self.Hidden_Divergence[s][2] = bars[0][4]
                            # Decrease the width counter
                            self.Hidden_Divergence[s][1] -= 1
                            # Check if width counter is zero
                            if self.Hidden_Divergence[s][1] == 0:
                                # Set Hidden Divergence to 0
                                self.Hidden_Divergence[s][0] = 0
                        # Bullish Hidden Divergence
                        if self.Hidden_Divergence[s][0] == 1:
                            # EMA below close
                            if self.EMA_value < bars[0][5]:
                                # Stochastic crossover
                                if self.prev_Stochastic_value[0] > self.prev_Stochastic_value[1] and \
                                        self.Stochastic_value[0] < self.Stochastic_value[1]:
                                    # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                    take_profit = bars[0][5] + ((bars[0][5] - self.Hidden_Divergence[s][2]) * 2)
                                    signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'LONG',
                                                         self.Hidden_Divergence[s][2], take_profit)
                                    self.events.put(signal)
                        # Bearish Hidden Divergence
                        elif self.Hidden_Divergence[s][0] == -1:
                            # EMA above close
                            if self.EMA_value > bars[0][5]:
                                # Stochastic crossover
                                if self.prev_Stochastic_value[0] > self.prev_Stochastic_value[1] and \
                                        self.Stochastic_value[0] < self.Stochastic_value[1]:
                                    # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                                    take_profit = bars[0][5] - ((self.Hidden_Divergence[s][2] - bars[0][5]) * 2)
                                    signal = SignalEvent(bars[0][0], self.bars.timeframe_list[0], bars[0][1], 'SHORT',
                                                         self.Hidden_Divergence[s][2], take_profit)
                                    self.events.put(signal)
