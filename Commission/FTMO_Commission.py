from ED_Backtester.Commission.Commission import Commission


class FTMO_Commission(Commission):
    """
    Calculates the fees of trading based on the
    FTMO fee structure for FOREX, in USD.

    Based on:
    https://ftmo.com/en/trading-crypto-and-indices/
    """

    def __init__(self):
        """
        Initialises the FTMO_Commission
        """

    def calculate_commission(self, fill_cost, quantity):
        """
        Calculates and returns the commission
        """
        full_cost = (quantity / 100000) * 3
        return full_cost
