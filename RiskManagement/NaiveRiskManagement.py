from ED_Backtester.RiskManagement.RiskManagement import RiskManagement

from ED_Backtester.Event import OrderEvent

from math import floor


class NaiveRiskManagement(RiskManagement):
    """
    The NaiveRiskManagement object is designed to send orders to
    a brokerage object with a constant quantity size blindly,
    i.e. without any risk management or position sizing. It is
    used to test simpler strategies such as BuyAndHoldStrategy.
    """
    def __init__(self, bars):
        self.bars = bars

    def generate_order(self, port, signal, stop_loss=None, take_profit=None):
        """
        Simply transacts an OrderEvent object as a constant quantity
        sizing of the signal object, without risk management or
        position sizing considerations.

        Parameters:
        signal - The SignalEvent signal information.
        """
        order = None

        symbol = signal.symbol
        timeframe = signal.timeframe
        direction = signal.signal_type
        # strength = signal.strength

        current_price = self.bars.get_latest_bars(symbol, timeframe, 1)[0][5]

        mkt_quantity = floor(100)
        cur_quantity = port.current_positions[symbol]
        order_type = 'MKT'

        if stop_loss == current_price:
            return
        if direction == "LONG":
            if stop_loss > take_profit:
                return
            if stop_loss > current_price:
                return
            if take_profit < current_price:
                return
        elif direction == "SHORT":
            if take_profit > stop_loss:
                return
            if stop_loss < current_price:
                return
            if take_profit > current_price:
                return

        if direction == 'LONG' and cur_quantity == 0:
            order = OrderEvent(symbol, timeframe, order_type, mkt_quantity, 'BUY', stop_loss, take_profit)
        if direction == 'SHORT' and cur_quantity == 0:
            order = OrderEvent(symbol, timeframe, order_type, mkt_quantity, 'SELL', stop_loss, take_profit)

        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, timeframe, order_type, abs(cur_quantity), 'SELL', stop_loss, take_profit, "Close")
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, timeframe, order_type, abs(cur_quantity), 'BUY', stop_loss, take_profit, "Close")
        return order
