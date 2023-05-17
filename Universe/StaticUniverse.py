from Universe.Universe import Universe


class StaticUniverse(Universe):
    """
    This Universe is static so the symbol list cannot be changed
    """

    def __init__(self, symbol_list, all_symbols):
        """
        Initialises the Static Universe.

        Parameters:
        symbol_list - The symbol list to start with
        all_symbols - The list of all available symbols sorted by category
        """
        self.symbol_list = symbol_list
        self.all_symbols = all_symbols
        self.advanced_symbol_list = {}

    def initialise_symbol_list(self, account_currency):
        for symbol in self.symbol_list:
            category = self.all_symbols.return_category(symbol)
            if category[0] == "Forex":
                checkpair = None
                value = 0
                switch = False
                if account_currency not in symbol:
                    checkpair = account_currency + symbol[3:6]
                    if checkpair not in self.symbol_list:
                        checkpair = symbol[3:6] + account_currency
                        if checkpair not in self.symbol_list:
                            checkpair = None
                            value = 1
                        else:
                            switch = True
                else:
                    if symbol[:3] is account_currency:
                        checkpair = symbol
                    else:
                        value = 1
                category.append([checkpair, value, switch])
            self.advanced_symbol_list[symbol] = category

    def change_symbol_list(self, new_symbol_list):
        self.symbol_list = self.symbol_list

    def append_symbol_list(self, symbol_list):
        self.symbol_list = self.symbol_list

    def return_symbol_list(self):
        return self.symbol_list

    def return_advanced_symbol_list(self):
        return self.advanced_symbol_list

    def return_advanced_symbol_stats(self, ticker):
        return self.advanced_symbol_list[ticker]
