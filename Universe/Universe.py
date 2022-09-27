from abc import ABCMeta, abstractmethod


class Universe(object):
    """
    Universe is an abstract base class to save and change
    the list of symbols to trade.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def change_symbol_list(self, new_symbol_list):
        """
        Changes the Symbol List
        """
        raise NotImplementedError("Should implement change_symbol_list()")

    @abstractmethod
    def append_symbol_list(self, symbol_list):
        """
        Appends Elements to the Symbol List
        """
        raise NotImplementedError("Should implement append_symbol_list()")

    @abstractmethod
    def return_symbol_list(self):
        """
        Returns the Symbol List
        """
        raise NotImplementedError("Should implement append_symbol_list()")
