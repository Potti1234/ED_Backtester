from ED_Backtester.Indicator.ATR import ATR
from ED_Backtester.Indicator.CPR import CPR
from ED_Backtester.Indicator.EMA import EMA
from ED_Backtester.Indicator.EngulfingCandle import EngulfingCandle
from ED_Backtester.Indicator.Hidden_Divergence import Hidden_Divergence
from ED_Backtester.Indicator.HighestLowest import HighestLowest
from ED_Backtester.Indicator.MACD import MACD
from ED_Backtester.Indicator.MajorSwingLevels import MajorSwingLevels
from ED_Backtester.Indicator.Pinbar import Pinbar
from ED_Backtester.Indicator.PinbarInsideBar import PinbarInsideBar
from ED_Backtester.Indicator.RSI import RSI
from ED_Backtester.Indicator.SMA import SMA
from ED_Backtester.Indicator.SR import SupportandResistance
from ED_Backtester.Indicator.Stochastic import Stochastic
from ED_Backtester.Indicator.TrendFilter import TrendFilter
from ED_Backtester.Indicator.VWAP import VWAP


def create_indicator(self, indicator):
    if indicator[0] == "RSI":
        self.set_save_periods(indicator[2], Close=True)

        for symbol in self.bars.universe.symbol_list:
            return RSI(indicator[1], symbol, indicator[2])
    elif indicator[0] == "SMA":
        self.set_save_periods(indicator[2], Close=True)

        for symbol in self.bars.universe.symbol_list:
            return SMA(indicator[1], symbol, indicator[2])
    elif indicator[0] == "EMA":
        self.set_save_periods(indicator[2], Close=True)

        for symbol in self.bars.universe.symbol_list:
            return EMA(indicator[1], symbol, indicator[2])
    elif indicator[0] == "VWAP":
        self.set_save_periods(indicator[2], Low=True, High=True, Close=True, Volume=True)

        for symbol in self.bars.universe.symbol_list:
            return VWAP(indicator[1], symbol, indicator[2])
    elif indicator[0] == "SR":
        self.set_save_periods(indicator[2], Low=True, High=True)

        for symbol in self.bars.universe.symbol_list:
            return SupportandResistance(indicator[1], symbol, indicator[2], indicator[3])
    elif indicator[0] == "ATR":
        self.set_save_periods(indicator[2], Low=True, High=True)

        for symbol in self.bars.universe.symbol_list:
            return ATR(indicator[1], symbol, indicator[2])
    elif indicator[0] == "Stochastic":
        self.set_save_periods(indicator[2], Low=True, High=True, Close=True)

        for symbol in self.bars.universe.symbol_list:
            return Stochastic(indicator[1], symbol, indicator[2], indicator[3])
    elif indicator[0] == "Hidden Divergence":
        self.set_save_periods(indicator[2], Close=True)

        for symbol in self.bars.universe.symbol_list:
            return Hidden_Divergence(indicator[1], symbol, indicator[2], indicator[3],
                                                                 indicator[4], indicator[5],
                                                                 self.create_indicator(indicator[6]))
    elif indicator[0] == "MACD":
        self.set_save_periods(indicator[2], Close=True)

        for symbol in self.bars.universe.symbol_list:
            return MACD(indicator[1], symbol, indicator[2], indicator[3], indicator[4])
    elif indicator[0] == "HighestLowest":
        self.set_save_periods(indicator[2], Low=True, High=True)

        for symbol in self.bars.universe.symbol_list:
            return HighestLowest(indicator[1], symbol, indicator[2])
    elif indicator[0] == "TrendFilter":
        self.set_save_periods(indicator[2], Low=True, High=True)

        for symbol in self.bars.universe.symbol_list:
            return TrendFilter(indicator[1], symbol, indicator[2], indicator[3], indicator[4], indicator[5], indicator[6], indicator[7])
    elif indicator[0] == "MajorSwingLevels":
        self.set_save_periods(indicator[2], Low=True, High=True, Close=True)

        for symbol in self.bars.universe.symbol_list:
            return MajorSwingLevels(indicator[1], symbol, indicator[2], indicator[3], indicator[4], indicator[5], indicator[6])
    elif indicator[0] == "Pinbar":
        self.set_save_periods(indicator[2], Open=True, Low=True, High=True, Close=True)

        for symbol in self.bars.universe.symbol_list:
            return Pinbar(indicator[1], symbol, indicator[2], indicator[3])
    elif indicator[0] == "PinbarInsideBar":
        self.set_save_periods(indicator[2], Open=True, Low=True, High=True, Close=True)

        for symbol in self.bars.universe.symbol_list:
            return PinbarInsideBar(indicator[1], symbol, indicator[2], indicator[3])
    elif indicator[0] == "EngulfingCandle":
        self.set_save_periods(indicator[2], Open=True, Close=True)

        for symbol in self.bars.universe.symbol_list:
            return EngulfingCandle(indicator[1], symbol, indicator[2])
    elif indicator[0] == "CPR":
        self.set_save_periods(indicator[2], Low=True, High=True, Close=True)

        for symbol in self.bars.universe.symbol_list:
            return CPR(indicator[1], symbol, indicator[2])
