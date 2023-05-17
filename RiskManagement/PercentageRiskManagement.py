from RiskManagement.RiskManagement import RiskManagement

from Event import OrderEvent


class PercentageRiskManagement(RiskManagement):
    """
    The PercentageRiskManagement object is designed to send orders to
    a brokerage object with a size calculated with a RiskPercentage,
     a Stop Loss, and the current price
    """
    def __init__(self, bars, risk_percent):
        self.bars = bars
        self.risk = risk_percent

    def generate_order(self, port, signal, stop_loss=None, take_profit=None, parameters=None):
        """
        Calculates the order size with the RiskPercentage, the Stop Loss
        and the current price

        Parameters:
        signal - The SignalEvent signal information.
        """
        if parameters is None:
            parameters = []
        order = None

        symbol = signal.symbol
        timeframe = signal.timeframe
        direction = signal.signal_type
        # strength = signal.strength

        current_cash = port.all_holdings[-1]["cash"]
        risk_amount = current_cash * (self.risk / 100)
        current_price = self.bars.get_latest_bars(symbol, timeframe, 1)[0][5]

        cur_quantity = port.current_positions[symbol][0]
        order_type = 'MKT'

        if direction == 'Change':
            order = OrderEvent(symbol, timeframe, "MKT", 0, 'Change', stop_loss, take_profit, "Change",
                               parameters=parameters)
            return order

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
            mkt_quantity = int(risk_amount / (current_price - stop_loss))
            order = OrderEvent(symbol, timeframe, order_type, mkt_quantity, 'BUY', stop_loss, take_profit,
                               parameters=parameters)
        if direction == 'SHORT' and cur_quantity == 0:
            mkt_quantity = int(risk_amount / (stop_loss - current_price))
            order = OrderEvent(symbol, timeframe, order_type, mkt_quantity, 'SELL', stop_loss, take_profit,
                               parameters=parameters)

        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, timeframe, order_type, abs(cur_quantity), 'SELL', stop_loss, take_profit,
                               "Close", parameters=parameters)
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, timeframe, order_type, abs(cur_quantity), 'BUY', stop_loss, take_profit,
                               "Close", parameters=parameters)
        return order
