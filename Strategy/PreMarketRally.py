from ED_Backtester.Event import SignalEvent
from ED_Backtester.Strategy.Strategy import Strategy


class PreMarketRally(Strategy):
    """
    Scanner Criterias:
    -Pre-Market
    -Price over 1$
    -Volume over 1000 shares
    -New High
    -Float lower than 50 Million
    -History of running
    -Day 1
    Entry Criterias:
    -First dip holds VWAP
    -Strong Buy Volume weak sell volume on dips
    -Breakout after dip
    -Spread is tight
    """

    def __init__(self, events, bars):
        """
        Initialises PreMarketRally strategy.

        Parameters:
        bars - The DataHandler object that provides bar information
        events - The Event Queue object.
        """
        self.bars = bars
        self.events = events

    def calculate_signals(self, event):
        """
        The PreMarketRally Strategy searches for Entries
        during the Premarket and Exits is price
        drops below VWAP

        Parameters
        event - A MarketEvent object.
        """

        if event.type == 'MARKET':
            for s in self.bars.universe.symbol_list:
                bars = self.bars.get_latest_bars(s, n=1)
                if bars is not None and bars != []:
                    print(0)
