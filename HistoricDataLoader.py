import datetime as dt
import pandas as pd
import requests
import json
from datetime import datetime
import time
from Symbol_lists import return_category

import pyhoo
import finnhub

Current_Datetime = int(dt.datetime.timestamp(dt.datetime.now()))


def get_historical_data_polygon(ticker, multiplier, timespan, startdate, enddate, limit, key):

    r = requests.get('https://api.polygon.io/v2/aggs/ticker/{}/range/{}/{}/{}/{}?limit={}&apiKey={}'.format(
        ticker, multiplier, timespan, startdate, enddate, limit, key))
    data = json.loads(r.content)

    Time = []
    Open = []
    high = []
    low = []
    close = []
    volume = []

    try:
        data["results"]
    except KeyError:
        print("No result")
        return

    for item in data['results']:

        Time.append(item['t']/1000)
        Open.append(item["o"])
        high.append(item["h"])
        low.append(item["l"])
        close.append(item["c"])
        volume.append(item["v"])

    d = {"datetime": Time, "open": Open, "low": low, "high": high, "close": close, "volume": volume}
    df = pd.DataFrame(data=d)

    return df


def get_historical_data_financial_modeling_prep(ticker, timeframe, start, end, key):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/{}/{}?from={}&to={}&apikey={}'.format(
        timeframe, ticker, start, end, key))
    data = json.loads(r.content)

    Time = []
    Open = []
    high = []
    low = []
    close = []
    volume = []

    for item in data:
        Time.append(time.mktime(datetime.strptime(item["date"], '%Y-%m-%d %H:%M:%S').timetuple()))
        Open.append(item["open"])
        high.append(item["high"])
        low.append(item["low"])
        close.append(item["close"])
        volume.append(item["volume"])

    d = {"datetime": Time, "open": Open, "low": low, "high": high, "close": close, "volume": volume}
    df = pd.DataFrame(data=d)

    return df


def get_daily_historical_data_financial_modeling_prep(ticker, start, end, key):
    r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/{}?from={}&to={}&apikey={}'.format(
        ticker, start, end, key))
    data = json.loads(r.content)

    Time = []
    Open = []
    high = []
    low = []
    close = []
    volume = []

    for item in data:
        Time.append(time.mktime(datetime.strptime(item["date"], '%Y-%m-%d %H:%M:%S').timetuple()))
        Open.append(item["open"])
        high.append(item["high"])
        low.append(item["low"])
        close.append(item["close"])
        volume.append(item["volume"])

    d = {"datetime": Time, "open": Open, "low": low, "high": high, "close": close, "volume": volume}
    df = pd.DataFrame(data=d)

    return df


def get_income_statement_financial_modeling_prep(statement_type, ticker, period, limit, key):
    # statement_type = "income-statement" or "balance-sheet-statement" or "cash-flow-statement"
    # period = "" for annual data
    # period = "?period=quarter" for quarterly data
    r = requests.get('https://financialmodelingprep.com/api/v3/{}/{}{}&limit={}&apikey={}'.format(
        statement_type, ticker, period, limit, key))
    data = json.loads(r.content)
    print(data)


def get_float_financial_modeling_prep(ticker, key):
    r = requests.get('https://financialmodelingprep.com/api/v4/shares_float?symbol={}&apikey={}'.format(ticker, key))
    data = json.loads(r.content)

    return data[0]["floatShares"]


def get_key_metrics_financial_modeling_prep(ticker, limit, period, key):
    """
    Args:
        ticker: The stock ticker
        limit: How many to return
        period: can be quaterly or None for yearly
        key: The api key

    Returns:
        The key financial metrics
    """
    if period is not None:
        r = requests.get("https://financialmodelingprep.com/api/v3/key-metrics/{}?period={}&limit={}&apikey={}".format(
            ticker, period, limit, key))
    else:
        r = requests.get("https://financialmodelingprep.com/api/v3/key-metrics/{}?limit={}&apikey={}".format(
            ticker, limit, key))

    data = json.loads(r.content)

    marketcap = []

    for item in data:
        marketcap.append(item["marketCap"])


def get_earnings_calendar_financial_modeling_prep(ticker, limit, start, end, key):
    # start and end cant be further away from each other than 3 months
    # if ticker is None all earnings in the timespan will be returned
    # if ticker has a value last limit amounts of earnings of this ticker will be returned
    if ticker is None:
        r = requests.get('https://financialmodelingprep.com/api/v3/earning_calendar?from={}&to={}&apikey={}'.format(
            start, end, key))
    else:
        r = requests.get('https://financialmodelingprep.com/api/v3/earning_calendar/{}?limit={}&apikey={}'.format(
            ticker, limit, key))
    data = json.loads(r.content)
    print(data)


def get_all_symbols_financial_modeling_prep(group_by, only_tradable, key):
    r = requests.get('https://financialmodelingprep.com/api/v3/stock/list?apikey={}'.format(key))
    data = json.loads(r.content)
    symbols = {}
    for symbol in data:
        if only_tradable is True and symbol["price"] == 0:
            continue
        try:
            symbols[symbol[group_by]].append(symbol["symbol"])
        except KeyError:
            symbols[symbol[group_by]] = [symbol["symbol"]]
    print(symbols)


def get_all_tradable_symbols_financial_modeling_prep(group_by, key):
    # group_by = "exchangeShortName" for exchange "type" for type(stock, etf)
    r = requests.get('https://financialmodelingprep.com/api/v3/available-traded/list?apikey={}'.format(key))
    data = json.loads(r.content)
    symbols = {}
    for symbol in data:
        try:
            symbols[symbol[group_by]].append(symbol["symbol"])
        except KeyError:
            symbols[symbol[group_by]] = [symbol["symbol"]]
    return symbols


def get_all_symbols_polygon(group_by, market, exchange, active, key):
    # market can be stocks, crypto, fx, otc
    # active can be true or false
    # exchange can be anything from this list https://www.iso20022.org/market-identifier-codes
    r = requests.get("https://api.polygon.io/v3/reference/tickers?market={}&exchange={}&active={}&limit=1000&apiKey={}".format(market, exchange, active, key))
    data = json.loads(r.content)
    data = data["results"]
    symbols = {}
    for symbol in data:
        try:
            symbols[symbol[group_by]].append(symbol["ticker"])
        except KeyError:
            symbols[symbol[group_by]] = [symbol["ticker"]]
    return symbols


def get_screener_financial_modeling_prep(conditions, key):
    # conditions can be marketcapmorethan, marketcaplowerthan, pricemorethan, pricelowerthan, betamorethan,
    # betalowerthan, volumemorethan, volumelessthan, dividendmorethan, dividendlessthan, isetf, isactifelytrading,
    # sector, industry, country, exchange, limit
    # format should be [[condition1name, condition1value], [condition2name, condition2value], ...]
    # parameter information at https://site.financialmodelingprep.com/developer/docs/stock-screener-api/#Python
    api_conditions = ""
    for parameter in conditions:
        api_conditions = api_conditions + parameter[0] + "=" + str(parameter[2]) + "&"

    r = requests.get('https://financialmodelingprep.com/api/v3/stock-screener?{}apikey={}'.format(api_conditions, key))
    data = json.loads(r.content)
    print(data)


def get_date_n_days_ago(n, date_to_start=Current_Datetime):
    date_n_days_ago = datetime.fromtimestamp(date_to_start) - dt.timedelta(days=n)
    date_n_days_ago = date_n_days_ago.strftime('%Y-%m-%d')
    return date_n_days_ago


def save_all_tickers(multiplier, period):
    df = pd.read_excel("D:/AktienDaten/tickers.xlsx")
    tickers = df["Name"].values
    for ticker in tickers:
        print(ticker)
        df = get_historical_data_polygon(ticker, multiplier, period, get_date_n_days_ago(730), get_date_n_days_ago(0),
                                         50000, 'pyEAjCqpC3onqokcA6Y4AVj1zx__c6zE_AKY8q')
        df.to_csv("D:/AktienDaten/{}{}/{}.csv".format(multiplier, period, ticker), index=False)
        time.sleep(13)


def save_1min_ticker(ticker, period=25):
    # period = days to look back times 30
    modified_ticker = ticker
    if "C:" in modified_ticker:
        modified_ticker = modified_ticker[2:]
    for i in range(period, 0, -1):
        print("{} from {} to {}".format(modified_ticker, get_date_n_days_ago(i * 30), get_date_n_days_ago((i - 1) * 30)))
        df = get_historical_data_polygon(ticker, 1, "minute", get_date_n_days_ago(i * 30),
                                         get_date_n_days_ago((i - 1) * 30), 50000,
                                         'pyEAjCqpC3onqokcA6Y4AVj1zx__c6zE_AKY8q')
        if df is None:
            time.sleep(12)
            continue
        try:
            dfold = pd.read_csv("D:/AktienDaten/{}{}/{}.csv".format(1, "minute", modified_ticker))
        except FileNotFoundError:
            dfold = pd.DataFrame(columns=["datetime", "open", "low", "high", "close", "volume"])

        dfold = dfold.append(df, ignore_index=True)
        dfold = dfold[~dfold.duplicated(subset="datetime")]
        dfold = dfold.sort_values("datetime")
        dfold = dfold[["datetime", "open", "low", "high", "close", "volume"]].apply(pd.to_numeric)
        dfold = dfold.set_index("datetime")
        dfold.to_csv("D:/AktienDaten/{}{}/{}.csv".format(1, "minute", modified_ticker))
        time.sleep(12)

    
def reformat_data(timeframe, ticker, append, start_dt, end_dt):
    # Get timeframe in seconds
    timeframe_in_sec = get_timeframe_in_sec(timeframe)

    df = pd.read_csv("D:/AktienDaten/1minute/{}.csv".format(ticker))
    df = df[df["datetime"] >= start_dt]
    df = df[df["datetime"] <= end_dt]
    df[["datetime", "open", "low", "high", "close", "volume"]] = df[
        ["datetime", "open", "low", "high", "close", "volume"]].apply(pd.to_numeric)

    if "Day" in timeframe:
        # Get day start time
        day_start_time = return_category(ticker)[1]
        # Convert day start time to seconds
        day_start_time = datetime.strptime(day_start_time, "%H:%M").timestamp()
        df["datetime"] = df["datetime"] - day_start_time

    df["CandleOpentime"] = df["datetime"] - (df["datetime"] % timeframe_in_sec)
    reformated_data = pd.DataFrame()
    reformated_data["datetime"] = df["datetime"]
    reformated_data["open"] = df.groupby("CandleOpentime")["open"].first().values.repeat(
        df.groupby("CandleOpentime").size())
    reformated_data["low"] = df.groupby("CandleOpentime")["low"].cummin()
    reformated_data["high"] = df.groupby("CandleOpentime")["high"].cummax()
    reformated_data["close"] = df["close"]
    reformated_data["volume"] = df.groupby("CandleOpentime")["volume"].cumsum()

    if append is True:
        df = pd.read_csv("D:/AktienDaten/{}/{}.csv".format(timeframe, ticker))
        df = df.append(reformated_data, ignore_index=True)
        df = df[~df.duplicated(subset="datetime")]
        df = df.sort_values("datetime")
        df = df[["datetime", "open", "low", "high", "close", "volume"]].apply(pd.to_numeric)
        df = df.set_index("datetime")
        df.to_csv("D:/AktienDaten/{}/{}.csv".format(timeframe, ticker))
        print(df)
    else:
        reformated_data.to_csv("D:/AktienDaten/{}/{}.csv".format(timeframe, ticker))
        print(reformated_data)


def ninjatrader_to_csv(filename, save_filename=None):
    df = pd.read_csv(filename, sep=";", header=None)
    df.columns = ["datetime", "open", "high", "low", "close", "volume"]
    dates = df["datetime"].values
    print(df)
    for i in range(len(dates)):
        dates[i] = dates[i][0:4] + "/" + dates[i][4:6] + "/" + dates[i][6:8] + " " + dates[i][9:11] + ":" + \
                   dates[i][11:13] + ":" + dates[i][13:15]
        dates[i] = time.mktime(datetime.strptime(dates[i], '%Y/%m/%d %H:%M:%S').timetuple())
        if i != 0:
            if dates[i-1] >= dates[i]:
                dates[i] += 60 * 60

    df = df[["datetime", "open", "low", "high", "close", "volume"]]
    if save_filename is not None:
        df.to_csv(save_filename)
    print(df)
    return df


def csv_to_ninjatrader(filename, save_filename):
    df = pd.read_csv(filename)
    print(df)
    dates = df["datetime"].values

    for i in range(len(dates)):
        dates[i] = datetime.fromtimestamp(dates[i])
        date = str(dates[i].year)
        if dates[i].month < 10:
            date = date + "0" + str(dates[i].month)
        else:
            date = date + str(dates[i].month)
        if dates[i].day < 10:
            date = date + "0" + str(dates[i].day)
        else:
            date = date + str(dates[i].day)
        date = date + " "
        if dates[i].hour < 10:
            date = date + "0" + str(dates[i].hour)
        else:
            date = date + str(dates[i].hour)
        if dates[i].minute < 10:
            date = date + "0" + str(dates[i].minute)
        else:
            date = date + str(dates[i].minute)
        if dates[i].second < 10:
            date = date + "0" + str(dates[i].second)
        else:
            date = date + str(dates[i].second)
        dates[i] = date

    df = df[["datetime", "open", "high", "low", "close", "volume"]]
    # print(df)
    df.to_csv(save_filename, sep=";", index=False, header=False)


def combine_year(year, start_month, end_month, ticker, folder="Forex Histdata"):
    df = pd.DataFrame()
    for i in range(start_month, end_month+1):
        month = str(i).zfill(2)
        file = "D:\\AktienDaten\\{}\\HISTDATA_COM_ASCII_{}_M1{}{}\\DAT_ASCII_{}_M1_{}{}.csv".format(
            folder, ticker, year, month, ticker, year, month)
        try:
            df_month = pd.read_csv(file, header=None)
            df = df.append(df_month, ignore_index=True)
        except FileNotFoundError:
            continue
    save_file = "D:\\AktienDaten\\{}\\DAT_ASCII_{}_M1_{}.csv".format(folder, ticker, year)
    df.to_csv(save_file, index=False, header=False)
    ninjatrader_to_csv(save_file, save_file)


def append_year(year, ticker, folder="Forex Histdata", filename="D:\\AktienDaten\\1minute\\"):
    file = "D:\\AktienDaten\\{}\\DAT_ASCII_{}_M1_{}.csv".format(folder, ticker, year)
    save_file = filename + ticker + ".csv"
    dfnew = pd.read_csv(file)
    df = pd.read_csv(save_file)
    print(len(df))
    df = df.append(dfnew, ignore_index=True)
    df = df[~df.duplicated(subset="datetime")]
    df = df.sort_values("datetime")
    df = df[["datetime", "open", "low", "high", "close", "volume"]].apply(pd.to_numeric)
    df = df.set_index("datetime")
    df.to_csv(save_file)
    print(len(df))


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


"""
start_date = "2018/01/01 00:00:00"
start_date = time.mktime(datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S').timetuple())
end_date = "2021/01/01 00:00:00"
end_date = time.mktime(datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S').timetuple())
reformat_data(5, "minute", "ES", 300, False, start_date, end_date)

df = pd.read_hdf("D:/AktienDaten/5minute/ES.h5")
df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
print(df)
"""
#save_1min_ticker("SPY")
#dfold = pd.read_hdf("D:/AktienDaten/{}{}/{}.h5".format(1, "minute", "ES"))
#print(dfold)

"""
ticker = "AMZN"
Multiplier = 7
Period = "day"
df = get_historical_data_polygon(ticker, Multiplier, Period, get_date_n_days_ago(365*5), get_date_n_days_ago(0), 'pyEAjCqpC3onqokcA6Y4AVj1zx__c6zE_AKY8q')
#df.to_hdf("D:/AktienDaten/{}{}/{}.h5".format(Multiplier,Period,ticker), key="df")
df.to_csv("D:/AktienDaten/{}{}/{}.csv".format(Multiplier,Period,ticker))
print(df)
"""
#df = pd.read_csv("D:/AktienDaten/7day/AMZN.csv")
#df["datetime"] = pd.to_datetime(df["datetime"], unit="s")

#print(df)
#save_all_tickers(1,"day")
#Ninjatrader_to_hdf("D:\\AktienDaten\\ES Histdata\\DAT_NT_SPXUSD_M1_2020.csv", 'D:\\AktienDaten\\1minute\\Test.h5')
#reformat_data(5, "minute", "ES", 300)

#hdf_to_Ninjatrader('D:\\AktienDaten\\1minute\\ES.h5', 'D:\\AktienDaten\\1minute\\ES 12-20.Last.txt')
#Ninjatrader_to_hdf('D:\\AktienDaten\\1minute\\ES 12-20.Last.txt', 'D:\\AktienDaten\\1minute\\ES.h5')

"""
tickers = ['AMZN']
start = '2016-04-22'
end = '2021-04-22'

stock_prices = pyhoo.get('chart', tickers, start=start, end=end, granularity="1d")
print(stock_prices)
stock_prices.to_csv("D:/AktienDaten/1day/AMZN.csv")

df = pd.read_csv("D:/AktienDaten/1day/AMZN.csv")
df = df.round(2)
print(df)
df.to_csv("D:/AktienDaten/1day/AMZN.csv")
"""
"""
for stock in Majors:
    filename = "D:\\AktienDaten\\Histdata\\HISTDATA_COM_NT_{}_M12019\\DAT_NT_{}_M1_2019.csv".format(stock, stock)
    df = ninjatrader_to_csv(filename, filename)
    filename = "D:\\AktienDaten\\Histdata\\HISTDATA_COM_NT_{}_M12020\\DAT_NT_{}_M1_2020.csv".format(stock, stock)
    df = df.append(ninjatrader_to_csv(filename, filename), ignore_index=True)

    for i in range(1, 8, 1):
        filename = "D:\\AktienDaten\\Histdata\\HISTDATA_COM_NT_{}_M120210{}\\DAT_NT_{}_M1_20210{}.csv".format(stock, i, stock, i)
        df = df.append(ninjatrader_to_csv(filename, filename), ignore_index=True)
    df.to_csv("D:\\AktienDaten\\Histdata\\{}.csv".format(stock))
    print(df)
"""

if __name__ == "__main__":
    financial_modeling_prep_api_key = "7a7b24b38a6be8117c47e1b979ec05cd"

    Majors = ["AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "AUDUSD", "CADCHF", "CADJPY", "CHFJPY", "EURAUD", "EURCAD",
              "EURCHF", "EURGBP", "EURJPY", "EURNZD", "EURUSD", "GBPAUD", "GBPCAD", "GBPCHF", "GBPJPY", "GBPNZD",
              "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD", "USDCAD", "USDCHF", "USDJPY"]

    # save_1min_ticker("AUDCAD", 10)
    # ninjatrader_to_csv("D:\\AktienDaten\\1minute\\EURUSDTest.csv", "D:\\AktienDaten\\1minute\\EURUSDTest.csv")
    start_date = "2021/08/01 00:00:00"
    start_date = time.mktime(datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S').timetuple())
    end_date = "2022/08/02 00:00:00"
    end_date = time.mktime(datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S').timetuple())

    symbol_list = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"]
    get_historical_data_financial_modeling_prep("AAPL", "1min", "2020-12-29", "2022-12-26", financial_modeling_prep_api_key)
    #get_daily_historical_data_financial_modeling_prep("AAPL", "2010-11-29", "2022-11-29", financial_modeling_prep_api_key)
    # get_float_financial_modeling_prep("AAPL", financial_modeling_prep_api_key)
    # get_all_symbols_financial_modeling_prep(financial_modeling_prep_api_key)
    #all_symbols = get_all_tradable_symbols_financial_modeling_prep("exchangeShortName", financial_modeling_prep_api_key)
    #for k, value in all_symbols.items():
    #    with open(r'C:\Users\lukas\OneDrive\Dokumente\Pottibot\Backtester\ED_Backtester\Symbols\{}.txt'.format(k), 'w') as fp:
    #        fp.write(','.join(value))
    #    print(k, value)

    #for s in Majors:
        #reformat_data(15, "minute", s, True, start_date, end_date)
        #reformat_data(4, "hour", s, True, start_date, end_date)

    #finnhub_client = finnhub.Client(api_key="c9irljaad3iblk5afv7g")
    #res = finnhub_client.stock_candles('AAPL', '1', int(start_date), int(end_date))
    #print(res)
    #print(finnhub_client.company_basic_financials('AAPL', 'all'))
    #print(finnhub_client.stock_symbols('US'))
