class Event(object):
    """
    Event is base class providing an interface for all subsequent 
    (inherited) events, that will trigger further events in the 
    trading infrastructure.   
    """
    pass


class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with 
    corresponding bars.
    """

    def __init__(self):
        """
        Initialises the MarketEvent.
        """
        self.type = 'MARKET'


class SignalEvent(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """
    
    def __init__(self, symbol, timeframe, datetime, signal_type, stop_loss=None, take_profit=None, parameters=None):
        """
        Initialises the SignalEvent.

        Parameters:
        symbol - The ticker symbol, e.g. 'GOOG'.
        timeframe - The timeframe
        datetime - The timestamp at which the signal was generated.
        signal_type - 'LONG' or 'SHORT' or 'EXIT'.
        """

        if parameters is None:
            parameters = []
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.timeframe = timeframe
        self.datetime = datetime
        self.signal_type = signal_type
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.parameters = parameters


class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    quantity and a direction.
    """

    def __init__(self, symbol, timeframe, order_type, quantity, direction, stop_loss=None, take_profit=None,
                 message="Open", parameters=None):
        """
        Initialises the order type, setting whether it is
        a Market order ('MKT') or Limit order ('LMT'), has
        a quantity (integral) and its direction ('BUY' or
        'SELL').

        Parameters:
        symbol - The instrument to trade.
        order_type - 'MKT' or 'LMT' for Market or Limit.
        quantity - Non-negative integer for quantity.
        direction - 'BUY' or 'SELL' for long or short.
        """

        if parameters is None:
            parameters = []
        self.type = 'ORDER'
        self.symbol = symbol
        self.timeframe = timeframe
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.message = message
        self.parameters = parameters
        # self.print_order()

    def print_order(self):
        """
        Outputs the values within the Order.
        """
        print("Order: Symbol=%s, Timeframe=%s, Type=%s, Quantity=%s, Direction=%s, Stop Loss=%s, Take Profit=%s" %
              (self.symbol, self.timeframe, self.order_type, self.quantity, self.direction, self.stop_loss, self.take_profit))


class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from a brokerage. Stores the quantity of an instrument
    actually filled and at what price. In addition, stores
    the commission of the trade from the brokerage.
    """

    def __init__(self, time_index, symbol, timeframe, exchange, quantity, direction, fill_cost, commission=None,
                 stop_loss=None, take_profit=None, message=None, parameters=None):
        """
        Initialises the FillEvent object. Sets the symbol, exchange,
        quantity, direction, cost of fill and an optional 
        commission.

        If commission is not provided, the Fill object will
        calculate it based on the trade size and Interactive
        Brokers fees.

        Parameters:
        time_index - The bar-resolution when the order was filled.
        symbol - The instrument which was filled.
        exchange - The exchange where the order was filled.
        quantity - The filled quantity.
        direction - The direction of fill ('BUY' or 'SELL')
        fill_cost - The holdings value in dollars.
        commission - An optional commission sent from IB.
        """

        if parameters is None:
            parameters = []
        self.type = 'FILL'
        self.time_index = time_index
        self.symbol = symbol
        self.timeframe = timeframe
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.commission = commission
        self.message = message
        self.parameters = parameters
