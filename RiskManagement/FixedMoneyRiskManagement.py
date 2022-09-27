from ED_Backtester.RiskManagement.RiskManagement import RiskManagement

from ED_Backtester.Event import OrderEvent


class FixedMoneyRiskManagement(RiskManagement):
    """
    The FixedMoneyRiskManagement object is designed to send orders to
    a brokerage object with a size calculated with a fixed amount of money,
    a Stop Loss, and the current price
    """
    def __init__(self, bars, risk_money):
        self.bars = bars
        self.risk = risk_money

    def generate_order(self, port, signal, stop_loss=None, take_profit=None, parameters=None):
        """
        Calculates the order size with the fixed amount of money, the Stop Loss
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

        current_price = self.bars.get_latest_bars(symbol, timeframe, 1)[0][5]

        cur_quantity = port.current_positions[symbol][0]
        order_type = 'MKT'
        if stop_loss is not None and take_profit is not None:
            if stop_loss == current_price:
                print("Stop Loss cant be current price")
                return
            if stop_loss <= 0:
                print("Stop Loss cant be smaller than 0")
                return
            if direction == "LONG":
                if stop_loss > take_profit:
                    print("LONG Stop Loss cant be bigger than Take Profit")
                    return
                if stop_loss > current_price:
                    print("LONG Stop Loss cant be bigger than entry price")
                    return
                if take_profit < current_price:
                    print("LONG Take Profit cant be smaller than entry price")
                    return
            elif direction == "SHORT":
                if take_profit > stop_loss:
                    print("SHORT Take Profit cant be bigger than Stop Loss")
                    return
                if stop_loss < current_price:
                    print("SHORT Stop Loss cant be smaller than entry price")
                    return
                if take_profit > current_price:
                    print("SHORT Take Profit cant be bigger than entry price")
                    return

        if cur_quantity == 0:
            # account currency first    risk * price / sl_pips * 10000
            # account currency second   risk / sl_pips * 10000
            # account currency not in symbol
            # use second currency to build pair
            # account currency first     risk * price / sl_pips * 10000
            # account currency second    risk / price / sl_pips * 10000
            # 10000 = 100 if JPY involved
            advanced_stats = self.bars.universe.return_advanced_symbol_stats(symbol)
            checkpair_price = advanced_stats[5][1]
            if checkpair_price == 0:
                checkpair_price = self.bars.get_latest_bars(advanced_stats[5][0], timeframe, 1)[0][5]
                if advanced_stats[5][2] is True:
                    checkpair_price = 1 / checkpair_price

            sl_size = abs(current_price - stop_loss)
            pip_size = advanced_stats[4]
            one_profit_size = 1 / pip_size
            sl_pips = sl_size / pip_size
            mkt_quantity = self.risk * checkpair_price / sl_pips * one_profit_size
            if mkt_quantity > 3300000:
                return
            if direction == 'LONG':
                order = OrderEvent(symbol, timeframe, order_type, mkt_quantity, 'BUY', stop_loss, take_profit,
                                   parameters=parameters)
            if direction == 'SHORT':
                order = OrderEvent(symbol, timeframe, order_type, mkt_quantity, 'SELL', stop_loss, take_profit,
                                   parameters=parameters)

        if direction == 'EXIT' and cur_quantity > 0:
            order = OrderEvent(symbol, timeframe, order_type, abs(cur_quantity), 'SELL', stop_loss, take_profit,
                               "Close", parameters=parameters)
        if direction == 'EXIT' and cur_quantity < 0:
            order = OrderEvent(symbol, timeframe, order_type, abs(cur_quantity), 'BUY', stop_loss, take_profit,
                               "Close", parameters=parameters)
        return order
