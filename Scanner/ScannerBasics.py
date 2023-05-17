import requests
import json
import bs4 as bs

from HistoricDataLoader import get_historical_data_polygon, get_date_n_days_ago


def check_History_of_Running(ticker, key):
    df = get_historical_data_polygon(ticker, 1, "day", get_date_n_days_ago(730), get_date_n_days_ago(0), key)
    Open = df["Open"].values()
    Close = df["Close"].values()

    Gaps_above_20 = 0

    for i in range(Close.lenght() - 1):
        Gap_Size = (Close[i] - Open[i+1]) / Open[i+1]
        if Gap_Size > 0.2:
            Gaps_above_20 = Gaps_above_20 + 1

    return Gaps_above_20


def Is_PreMarket(key):
    r = requests.get("https://api.polygon.io/v1/marketstatus/now?apiKey={}".format(key))
    data = json.loads(r.content)
    if data["market"] == "extended-hours":
        return True
    else:
        return False


def get_Float(ticker):
    """
    Retrieves the Float of a ticker from yahoo finance

    Parameters
    Ticker - The stock ticker

    Returns
    Float of the ticker
    """
    r = requests.get("https://finance.yahoo.com/quote/{}/key-statistics?p={}".format(ticker, ticker))
    soup = bs.BeautifulSoup(r.text, 'lxml')
    Float = soup.find_all("tr", {"class": "Bxz(bb) H(36px) BdB Bdbc($seperatorColor)"})[8].text
    Float = Float.replace("Float", "")
    if "K" in Float:
        Float = Float.replace("K", "")
        Float = float(Float)*1000
    elif "M" in Float:
        Float = Float.replace("M", "")
        Float = float(Float)*1000000
    elif "B" in Float:
        Float = Float.replace("B", "")
        Float = float(Float) * 1000000000
    elif "T" in Float:
        Float = Float.replace("T", "")
        Float = float(Float) * 1000000000000
    return int(Float)


def get_Market_Cap(ticker):
    """
    Retrieves the Market Cap of a ticker from yahoo finance

    Parameters
    Ticker - The stock ticker

    Returns
    Market Cap of the ticker
    """

    r = requests.get("https://finance.yahoo.com/quote/{}?p={}".format(ticker, ticker))
    soup = bs.BeautifulSoup(r.text, 'lxml')
    MC = soup.find_all("tr", {"class": "Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($seperatorColor) H(36px)"})[7].text
    MC = MC.replace("Market Cap", "")
    if "K" in MC:
        MC = MC.replace("K", "")
        MC = float(MC) * 1000
    elif "M" in MC:
        MC = MC.replace("M", "")
        MC = float(MC) * 1000000
    elif "B" in MC:
        MC = MC.replace("B", "")
        MC = float(MC) * 1000000000
    elif "T" in MC:
        MC = MC.replace("T", "")
        MC = float(MC) * 1000000000000
    return int(MC)
