import datetime

from ED_Backtester.Event import FillEvent
from ED_Backtester.Execution.Execution import ExecutionHandler


class SimulatedExecutionHandler(ExecutionHandler):
    """
    The simulated execution handler simply converts all order
    objects into their equivalent fill objects automatically
    without latency, slippage or fill-ratio issues.

    This allows a straightforward "first go" test of any strategy,
    before implementation with a more sophisticated execution
    handler.
    """

    def __init__(self, events, commission):
        """
        Initialises the handler, setting the event queues
        up internally.

        Parameters:
        events - The Queue of Event objects.
        """
        self.events = events
        self.commission = commission

    def execute_order(self, event):
        """
        Simply converts Order objects into Fill objects naively,
        i.e. without any latency, slippage or fill ratio problems.

        Parameters:
        event - Contains an Event object with order information.
        """
        if event.type == 'ORDER':
            fill_event = FillEvent(datetime.datetime.utcnow(), event.symbol, event.timeframe, 'ARCA', event.quantity,
                                   event.direction, 0, self.commission.calculate_commission(0, event.quantity),
                                   event.stop_loss, event.take_profit, event.message, event.parameters)
            self.events.put(fill_event)
