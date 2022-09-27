from abc import ABCMeta, abstractmethod


class DataHandler(object):
    """
    DataHandler is an abstract base class providing an interface for
    all subsequent (inherited) data handlers (both live and historic).

    The goal of a (derived) DataHandler object is to output a generated
    set of bars (OLHCVI) for each symbol requested. 

    This will replicate how a live strategy would function as current
    market data would be sent "down the pipe". Thus a historic and live
    system will be treated identically by the rest of the backtesting suite.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_latest_bars(self, symbol, timeframe, N=1):
        """
        Returns the last N bars from the latest_symbol list,
        or fewer if less bars are available.
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def update_bars(self):
        """
        Pushes the latest bar to the latest symbol structure
        for all symbols in the symbol list.
        """
        raise NotImplementedError("Should implement update_bars()")

    @staticmethod
    def get_timeframe_in_sec(timeframe):
        """
        Convert the string timeframe int a int value
        Args:
            timeframe: the timeframe to convert

        Returns:
            int: seconds of the timeframe

        """
        seconds = 0
        if "minute" in timeframe:
            seconds = 60
            timeframe = timeframe.replace("minute", "")
        elif "hour" in timeframe:
            seconds = 60*60
            timeframe = timeframe.replace("hour", "")
        elif "day" in timeframe:
            seconds = 60*60*24
            timeframe = timeframe.replace("day", "")

        return seconds * int(timeframe)
