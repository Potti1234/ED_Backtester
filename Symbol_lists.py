def return_forexpairs():
    return ["AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD",
            "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
            "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]


def return_jpy_forexpairs():
    return ["AUDJPY", "CADJPY", "CHFJPY", "EURJPY", "GBPJPY", "NZDJPY", "USDJPY"]


def return_5majors():
    return ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]


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
