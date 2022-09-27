from abc import ABCMeta, abstractmethod


class RiskManagement(object):
    """
    The RiskManagement class generates new orders
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_order(self, port, event):
        """
        Acts on a SignalEvent to generate new orders
        based on the RiskManagement logic.
        """
        raise NotImplementedError("Should implement generate_order()")
