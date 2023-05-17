import pandas as pd


class Symbols:
    def __init__(self):
        self.symbol_list = []
        self.add_jpy_pairs()
        self.add_forex_pairs()
        self.add_stocks()
        self.add_futures()

    def add_forex_pairs(self):
        self.symbol_list.append(return_forexpairs())

    def return_forex_pairs(self):
        return self.symbol_list[1]

    def add_jpy_pairs(self):
        self.symbol_list.append(return_jpy_forexpairs())

    def return_jpy_pairs(self):
        return self.symbol_list[0]

    def add_stocks(self):
        self.symbol_list.append(return_stocks())

    def return_stocks(self):
        return self.symbol_list[2]

    def add_futures(self):
        self.symbol_list.append(return_futures())

    def return_futures(self):
        return self.symbol_list[3]

    def return_category(self, ticker):
        # returns the parameters of the symbol Type, Open time, Close time, Premarket Open time, pip size, margin
        if ticker in self.symbol_list[0]:
            return ["Forex", "0:00", "24:00", "0:00", 0.01]
        elif ticker in self.symbol_list[1]:
            return ["Forex", "0:00", "24:00", "0:00", 0.0001]
        elif ticker in self.symbol_list[3]:
            return ["Futures", "0:00", "24:00", "0:00", 0.25]
        elif ticker in self.symbol_list[2]:
            return ["Stocks", "9:30", "16:00", "4:00", 0.01]
        elif ticker == "Crypto":
            return ["Crypto", "0:00", "24:00", "0:00", 0.01]


def return_forexpairs():
    return ["AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD",
            "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
            "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]


def return_jpy_forexpairs():
    return ["AUDJPY", "CADJPY", "CHFJPY", "EURJPY", "GBPJPY", "NZDJPY", "USDJPY"]


def return_5majors():
    return ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]


def return_futures():
    return ["ES"]


def return_stocks():
    stocks = pd.read_csv(r'C:\Users\lukas\OneDrive\Dokumente\Pottibot\Backtester\ED_Backtester\Symbols\NYSE.txt',
                         sep=",", header=None).iloc[0].to_list()
    return stocks


def return_category(ticker):
    # returns the parameters of the symbol Type, Open time, Close time, Premarket Open time, pip size, margin
    if ticker in return_jpy_forexpairs():
        return ["Forex", "0:00", "24:00", "0:00", 0.01]
    elif ticker in return_forexpairs():
        return ["Forex", "0:00", "24:00", "0:00", 0.0001]
    elif ticker == "Stocks":
        return ["Stocks", "9:30", "16:00", "4:00", 0.01]
    elif ticker == "Crypto":
        return ["Crypto", "0:00", "24:00", "0:00", 0.01]
    elif ticker == "Futures":
        return ["Futures", "0:00", "24:00", "0:00", 0.25]
