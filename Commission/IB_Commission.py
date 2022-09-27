from ED_Backtester.Commission.Commission import Commission


class IB_Commission(Commission):
    """
    Calculates the fees of trading based on an Interactive
    Brokers fee structure for API, in USD.

    This does not include exchange or ECN fees.

    Based on "US API Directed Orders":
    https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2
    """

    def __init__(self):
        """
        Initialises the IB_Commission
        """

    def calculate_commission(self, fill_cost, quantity):
        """
        Calculates and returns the commission
        """
        # print(fill_cost)
        if quantity <= 500:
            full_cost = max(1.3, 0.013 * quantity)
        else:  # Greater than 500
            full_cost = max(1.3, 0.008 * quantity)
        full_cost = min(full_cost, 0.5 / 100.0 * quantity * fill_cost)
        return full_cost
