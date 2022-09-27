from abc import ABCMeta, abstractmethod


class Scanner(object):
    """
    The Scanner class tries to find stocks to trade based on
    predefined criteria.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def scan_results(self):
        """
        Provides the mechanisms to calculate the list of stocks to trade.

        returns a list of stocks that match the criteria
        """
        raise NotImplementedError("Should implement scan_results()")
