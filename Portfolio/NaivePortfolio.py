import pandas as pd

from ED_Backtester.Event import SignalEvent

from ED_Backtester.Statistics.Performance import create_sharpe_ratio, create_drawdowns, create_cagr, \
    create_sortino_ratio
from ED_Backtester.Portfolio.portfolio import Portfolio


class NaivePortfolio(Portfolio):
    """
    The NaivePortfolio object is designed to send orders to
    a brokerage object with a constant quantity size blindly,
    i.e. without any risk management or position sizing. It is
    used to test simpler strategies such as BuyAndHoldStrategy.
    """

    def __init__(self, bars, events, start_date, risk_management, initial_capital=100000.0):
        """
        Initialises the Portfolio with bars and an event queue.
        Also includes a starting datetime index and initial capital
        (USD unless otherwise stated).

        Parameters:
        bars - The DataHandler object with current market data.
        events - The Event Queue object.
        start_date - The start date (bar) of the Portfolio.
        initial_capital - The starting capital in USD.
        """
        self.bars = bars
        self.events = events
        self.timeframe_list = self.bars.timeframe_list
        self.start_date = start_date
        self.RiskManagement = risk_management
        self.initial_capital = initial_capital

        self.equity_curve = pd.DataFrame()

        self.parameter_len = 0
        self.best_price_tp = {k: [] for k in self.bars.universe.symbol_list}
        self.best_price_sl = {k: [] for k in self.bars.universe.symbol_list}
        self.trade_amount = {k: 0 for k in self.bars.universe.symbol_list}

        # Creates the trades dictionary that saves the datetime price and size(+ or -) of each trade
        self.Trades = {s: {t: [] for t in self.timeframe_list} for s in self.bars.universe.symbol_list}

        self.all_positions = self.construct_all_positions()
        self.current_positions = dict((k, v) for k, v in [(s, [0, None, None]) for s in self.bars.universe.symbol_list])

        self.all_holdings = self.construct_all_holdings()
        self.current_holdings = self.construct_current_holdings()

    def construct_all_positions(self):
        """
        Constructs the positions list using the start_date
        to determine when the time index will begin.
        """
        d = dict((k, v) for k, v in [(s, 0) for s in self.bars.universe.symbol_list])
        d['datetime'] = self.start_date
        return [d]

    def construct_all_holdings(self):
        """
        Constructs the holdings list using the start_date
        to determine when the time index will begin.
        """
        d = dict((k, v) for k, v in [(s, 0.0) for s in self.bars.universe.symbol_list])
        d['datetime'] = self.start_date
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return [d]

    def construct_current_holdings(self):
        """
        This constructs the dictionary which will hold the instantaneous
        value of the Portfolio across all symbols.
        """
        d = dict((k, v) for k, v in [(s, 0.0) for s in self.bars.universe.symbol_list])
        d['cash'] = self.initial_capital
        d['commission'] = 0.0
        d['total'] = self.initial_capital
        return d

    def update_timeindex(self):
        """
        Adds a new record to the positions matrix for the current
        market data bar. This reflects the PREVIOUS bar, i.e. all
        current market data at this stage is known (OLHCVI).

        Makes use of a MarketEvent from the events queue.
        """
        bars = {}
        for s in self.bars.universe.symbol_list:
            bars[s] = self.bars.get_latest_bars(s, self.timeframe_list[0], n=1)

        # Checks if Stop Loss or Take Profit is hit
        self.check_sl_tp(bars)

        # Check best tp price
        self.calculate_best_tp_price(bars)

        # Check best sl price
        self.calculate_best_sl_price(bars)

        # Update positions
        dp = dict((k, v) for k, v in [(s, 0) for s in self.bars.universe.symbol_list])
        dp['datetime'] = bars[self.bars.universe.symbol_list[0]][0][1]

        for s in self.bars.universe.symbol_list:
            dp[s] = self.current_positions[s][0]

        # Append the current positions
        self.all_positions.append(dp)

        # Update holdings
        dh = dict((k, v) for k, v in [(s, 0) for s in self.bars.universe.symbol_list])
        dh['datetime'] = bars[self.bars.universe.symbol_list[0]][0][1]
        dh['cash'] = self.current_holdings['cash']
        dh['commission'] = self.current_holdings['commission']
        dh['total'] = self.current_holdings['cash']

        for s in self.bars.universe.symbol_list:
            if bars[s] != [] and bars[s] is not None:
                # Approximation to the real value in position currency
                market_value = self.current_positions[s][0] * bars[s][0][5]
                # Calculate real value
                advanced_stats = self.bars.universe.return_advanced_symbol_stats(s)

                checkpair_price = advanced_stats[5][1]
                if checkpair_price == 0:
                    checkpair_price = self.bars.get_latest_bars(advanced_stats[5][0], self.timeframe_list[0])[0][5]
                    if advanced_stats[5][2] is True:
                        checkpair_price = 1 / checkpair_price

                market_value = market_value / checkpair_price
                dh[s] = market_value
                dh['total'] += market_value

        # Append the current holdings
        self.all_holdings.append(dh)

    def calculate_best_tp_price(self, bars):
        for s in self.bars.universe.symbol_list:
            for i in self.best_price_tp[s]:
                # Buy trade
                if i[0] > 0:
                    # current price is bigger than sl
                    if i[1] < bars[s][0][3]:
                        self.Trades[s][i[3]][i[2]*2-2][8] = max(self.Trades[s][i[3]][i[2]*2-2][8], bars[s][0][4])
                    else:
                        self.best_price_tp[s].remove(i)
                # Sell trade
                elif i[0] < 0:
                    # current price is smaller than sl
                    if i[1] > bars[s][0][4]:
                        self.Trades[s][i[3]][i[2]*2-2][8] = min(self.Trades[s][i[3]][i[2]*2-2][8], bars[s][0][3])
                    else:
                        self.best_price_tp[s].remove(i)

    def calculate_best_sl_price(self, bars):
        for s in self.bars.universe.symbol_list:
            for i in self.best_price_sl[s]:
                # Buy trade
                if i[0] > 0:
                    # high price is smaller than tp
                    if i[1] > bars[s][0][4]:
                        self.Trades[s][i[3]][i[2]*2-2][9] = min(self.Trades[s][i[3]][i[2]*2-2][9], bars[s][0][3])
                    else:
                        self.best_price_sl[s].remove(i)
                # Sell trade
                elif i[0] < 0:
                    # low price is bigger than tp
                    if i[1] < bars[s][0][3]:
                        self.Trades[s][i[3]][i[2]*2-2][9] = max(self.Trades[s][i[3]][i[2]*2-2][9], bars[s][0][4])
                    else:
                        self.best_price_sl[s].remove(i)

    def check_sl_tp(self, bars):
        for s in self.bars.universe.symbol_list:
            if self.current_positions[s][0] != 0:
                # A Stop Loss is set
                if self.current_positions[s][1] is not None:
                    # It is a short position
                    if self.current_positions[s][0] < 0:
                        # Stop Loss is hit
                        if bars[s][0][4] > self.current_positions[s][1]:
                            signal = SignalEvent(bars[s][0][0], self.timeframe_list[0], bars[s][0][1], 'EXIT',
                                                 stop_loss=self.current_positions[s][1])
                            self.current_positions[s][1] = None
                            self.events.put(signal)
                    # It is a long position
                    elif self.current_positions[s][0] > 0:
                        # Stop Loss is hit
                        if bars[s][0][3] < self.current_positions[s][1]:
                            signal = SignalEvent(bars[s][0][0], self.timeframe_list[0], bars[s][0][1], 'EXIT',
                                                 stop_loss=self.current_positions[s][1])
                            self.current_positions[s][1] = None
                            self.events.put(signal)

                # A Take Profit is set
                if self.current_positions[s][2] is not None:
                    # It is a short position
                    if self.current_positions[s][0] < 0:
                        # Take Profit is hit
                        if bars[s][0][3] < self.current_positions[s][2]:
                            signal = SignalEvent(bars[s][0][0], self.timeframe_list[0], bars[s][0][1], 'EXIT',
                                                 take_profit=self.current_positions[s][2])
                            self.current_positions[s][2] = None
                            self.events.put(signal)
                    # It is a long position
                    elif self.current_positions[s][0] > 0:
                        # Take Profit is hit
                        if bars[s][0][4] > self.current_positions[s][2]:
                            signal = SignalEvent(bars[s][0][0], self.timeframe_list[0], bars[s][0][1], 'EXIT',
                                                 take_profit=self.current_positions[s][2])
                            self.current_positions[s][2] = None
                            self.events.put(signal)

    def update_positions_from_fill(self, fill):
        """
        Takes a FillEvent object and updates the position matrix
        to reflect the new position.

        Parameters:
        fill - The FillEvent object to update the positions with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update positions list with new quantities
        self.current_positions[fill.symbol][0] += fill_dir * fill.quantity
        # Update positions list with new Stop Loss, Take Profit
        if self.current_positions[fill.symbol][0] == 0:
            # if a trade got closed set the Stop Loss and Take Profit to None
            self.current_positions[fill.symbol][1] = None
            self.current_positions[fill.symbol][2] = None
        else:
            if fill.stop_loss is not None:
                self.current_positions[fill.symbol][1] = fill.stop_loss
            if fill.take_profit is not None:
                self.current_positions[fill.symbol][2] = fill.take_profit

    def update_holdings_from_fill(self, fill):
        """
        Takes a FillEvent object and updates the holdings matrix
        to reflect the holdings value.

        Parameters:
        fill - The FillEvent object to update the holdings with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction == 'BUY':
            fill_dir = 1
        if fill.direction == 'SELL':
            fill_dir = -1

        # Update holdings list with new quantities
        latest_bar = self.bars.get_latest_bars(fill.symbol, fill.timeframe)

        if fill.fill_cost == 0:
            # If there is no fill cost use the close price
            fill_cost = latest_bar[0][5]
            # Use TP or SL if it is a close
            if fill.message == "Close":
                # Use the value which is not None
                if fill.stop_loss is not None:
                    fill_cost = fill.stop_loss
                elif fill.take_profit is not None:
                    fill_cost = fill.take_profit
        else:
            fill_cost = fill.fill_cost
        # Approximation to the real cost in position currency
        cost = fill_dir * fill_cost * fill.quantity
        # Calculate real value in account currency
        advanced_stats = self.bars.universe.return_advanced_symbol_stats(fill.symbol)

        checkpair_price = advanced_stats[5][1]
        if checkpair_price == 0:
            checkpair_price = self.bars.get_latest_bars(advanced_stats[5][0], fill.timeframe)[0][5]
            if advanced_stats[5][2] is True:
                checkpair_price = 1 / checkpair_price

        cost = cost / checkpair_price
        # update holdings with cost
        self.current_holdings[fill.symbol] += cost
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cost + fill.commission)
        self.current_holdings['total'] -= (cost + fill.commission)
        # Update best price
        if fill.message != "Close":
            self.trade_amount[fill.symbol] += 1
            self.best_price_tp[fill.symbol].append([fill_dir, fill.stop_loss, self.trade_amount[fill.symbol],
                                                    fill.timeframe])
            self.best_price_sl[fill.symbol].append([fill_dir, fill.take_profit, self.trade_amount[fill.symbol],
                                                    fill.timeframe])

        # Update the trades dict with the new trade
        parameters = [latest_bar[0][1], fill_cost, fill_dir * fill.quantity, fill.commission, fill.stop_loss,
                      fill.take_profit, fill.message, fill.symbol, latest_bar[0][5], latest_bar[0][5]]
        if not fill.parameters:
            for i in range(self.parameter_len):
                parameters.append(0)
        else:
            self.parameter_len = len(fill.parameters)
            for variable in fill.parameters:
                parameters.append(variable)
        self.Trades[fill.symbol][fill.timeframe].append(parameters)

    def update_fill(self, event):
        """
        Updates the Portfolio current positions and holdings
        from a FillEvent.
        """
        if event.type == 'FILL':
            self.update_positions_from_fill(event)
            self.update_holdings_from_fill(event)

    def update_signal(self, event):
        """
        Acts on a SignalEvent to generate new orders
        based on the Portfolio logic.
        """
        if event.type == 'SIGNAL':
            order_event = self.RiskManagement.generate_order(self, event, event.stop_loss, event.take_profit,
                                                             parameters=event.parameters)
            if order_event is not None:
                self.events.put(order_event)

    def get_equity_curve(self):
        """
        Returns the equity curve as a Pandas DataFrame.
        Returns
        -------
        `pd.DataFrame`
            The datetime-indexed equity curve of the strategy.
        """
        self.create_equity_curve_dataframe()

        equity_df = pd.DataFrame()
        equity_df["total"] = self.equity_curve["total"]
        equity_df["datetime"] = self.equity_curve.index
        # equity_df.set_index('datetime')

        return equity_df

    def create_equity_curve_dataframe(self):
        """
        Creates a pandas DataFrame from the all_holdings
        list of dictionaries.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index('datetime', inplace=True)
        curve['returns'] = curve['total'].pct_change()
        curve['equity_curve'] = (1.0 + curve['returns']).cumprod()
        self.equity_curve = curve

    def output_summary_stats(self):
        """
        Creates a list of summary statistics for the Portfolio such
        as Sharpe Ratio and drawdown information.
        """
        total_return = self.equity_curve['equity_curve'][-1]
        returns = self.equity_curve['returns']
        pnl = self.equity_curve['equity_curve']
        total = self.equity_curve["total"]

        sharpe_ratio = create_sharpe_ratio(returns)
        dd, max_dd, dd_duration = create_drawdowns(pnl)
        cagr = create_cagr(total)
        sortino_ratio = create_sortino_ratio(returns)

        print(self.equity_curve)

        stats = [("Total Return", "%0.2f%%" % ((total_return - 1.0) * 100.0)),
                 ("Compound Annual Growth Rate", "%0.2f" % cagr),
                 ("Sharpe Ratio", "%0.2f" % sharpe_ratio),
                 ("Sortino Ratio", "%0.2f" % sortino_ratio),
                 ("Max Drawdown", "%0.2f%%" % (max_dd * 100.0)),
                 ("Drawdown Duration", "%d" % dd_duration)]
        return stats
