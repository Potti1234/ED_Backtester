from Indicator.ATR import ATR
from Indicator.CPR import CPR
from Indicator.EMA import EMA
from Indicator.EngulfingCandle import EngulfingCandle
from Indicator.Hidden_Divergence import Hidden_Divergence
from Indicator.HighestLowest import HighestLowest
from Indicator.MACD import MACD
from Indicator.MajorSwingLevels import MajorSwingLevels
from Indicator.Pinbar import Pinbar
from Indicator.PinbarInsideBar import PinbarInsideBar
from Indicator.RSI import RSI
from Indicator.SMA import SMA
from Indicator.SR import SupportandResistance
from Indicator.Stochastic import Stochastic
from Indicator.TrendFilter import TrendFilter
from Indicator.VWAP import VWAP
from Indicator.Range_filter import Range_filter


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
    elif indicator[0] == "Range_Filter":
        self.set_save_periods(indicator[2], Close=True)

        for symbol in self.bars.universe.symbol_list:
            return Range_filter(indicator[1], symbol, indicator[2], indicator[3], indicator[4])
