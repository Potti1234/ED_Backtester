from abc import ABCMeta, abstractmethod


class Commission(object):
    """
    The Commission class calculates the commissions
     which need to be paid
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def calculate_commission(self, fill_cost, quantity):
        """
        Calculates and returns the commission
        """
        raise NotImplementedError("Should implement calculate_commission()")
