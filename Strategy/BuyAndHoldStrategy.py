from Event import SignalEvent
from Strategy.Strategy import Strategy


class BuyAndHoldStrategy(Strategy):
    """
    This is an extremely simple strategy that goes LONG all of the
    symbols as soon as a bar is received. It will never exit a position.

    It is primarily used as a testing mechanism for the Strategy class
    as well as a benchmark upon which to compare other strategies.
    """

    def __init__(self, events, bars):
        """
        Initialises the buy and hold strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events

        # Once buy & hold signal is given, these are set to True
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        """
        Adds keys to the bought dictionary for all symbols
        and sets them to False.
        """
        bought = {}
        for s in self.bars.universe.symbol_list:
            bought[s] = False
        return bought

    def calculate_signals(self, event):
        """
        For "Buy and Hold" we generate a single signal per symbol
        and then no additional signals. This means we are
        constantly long the market from the date of strategy
        initialisation.

        Parameters
        event - A MarketEvent object.
        """
        if event.type == 'MARKET':
            for s in self.bars.universe.symbol_list:
                bars = self.bars.get_latest_bars(s, "30minute", n=1)
                # print(bars)
                if bars is not None and bars != []:
                    if self.bought[s] is False:
                        # (Symbol, Timeframe, Datetime, Type = LONG, SHORT or EXIT)
                        signal = SignalEvent(bars[0][0], "30minute", bars[0][1], 'LONG', stop_loss=bars[0][4], take_profit=bars[0][4])
                        self.events.put(signal)
                        self.bought[s] = True
