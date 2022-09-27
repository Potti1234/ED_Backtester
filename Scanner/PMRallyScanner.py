import datetime as dt

from ED_Backtester.Scanner.Scanner import Scanner
from ED_Backtester.Scanner.ScannerBasics import Is_PreMarket, get_Float, check_History_of_Running


class PMRallyScanner(Scanner):
    """
    Scans the market for potential Pre Market Rally Setups
    -Pre-Market
    -Price over 1$
    -Volume over 1000 shares
    -New High
    -Float lower than 50 Million
    -History of running
    -Day 1
    """

    def __init__(self, bars, scan_list):
        """

        Args:
            bars: the DataHandler object
            scan_list: The list of stocks to scan
        """
        self.time = int(dt.datetime.timestamp(dt.datetime.now()))
        self.bars = bars
        self.scan_list = scan_list
        self.key = 'pyEAjCqpC3onqokcA6Y4AVj1zx__c6zE_AKY8q'

    def scan_results(self):
        ScanResults = []
        self.time = int(dt.datetime.timestamp(dt.datetime.now()))
        # Check if it is PreMarket Time
        if Is_PreMarket(self.key):
            # Retrieve Price data
            Prices = self.bars.get_Aggregate_Price_Data()
            for ticker in Prices:
                DayData = ticker["day"]
                MinData = ticker["min"]
                # Check for New High
                if MinData["h"] >= DayData["h"]:
                    # Check if Price is above 1 $
                    if MinData["c"] >= 1:
                        # Check if Volume is over 1000
                        if DayData["v"] > 1000:
                            # Check if its on day one
                            PrevDayData = ticker["prevDay"]
                            if ((PrevDayData["c"]/PrevDayData["o"]) > 0.9) | ((PrevDayData["c"]/PrevDayData["o"]) < 1.1):
                                # Check if Float is lower than 50 Million
                                if get_Float(ticker["ticker"]) < 50000000:
                                    # Check History of Running
                                    if check_History_of_Running(ticker["ticker"], self.key) > 0:
                                        ScanResults.append(ticker["ticker"])

        return ScanResults
