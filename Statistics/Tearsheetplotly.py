import numpy as np

import Statistics.Performance as Perf
import Statistics.Plotting_Plotly as Plot
from Statistics.Statistics import Statistics

import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objects as go


class Tearsheetplotly(Statistics):
    """
    Displays a Plotly-generated 'one-pager' as often
    found in institutional strategy performance reports.
    """
    def __init__(self, portfolio, portfolio_benchmark=None, title=None, periods=252):
        self.port = portfolio
        self.port_bench = portfolio_benchmark
        self.title = title
        self.periods = periods

    def get_results(self, equity_df):
        """
        Return a dict with all important results & stats.
        """
        # Returns
        equity_df["returns"] = equity_df["total"].pct_change().fillna(0.0)

        # Cummulative Returns
        equity_df["cum_returns"] = np.exp(np.log(1 + equity_df["returns"]).cumsum())

        # Drawdown, max drawdown, max drawdown duration
        dd_s, max_dd, dd_dur = Perf.create_drawdowns(equity_df["cum_returns"])

        # Equity statistics
        statistics = {}
        statistics["sharpe"] = Perf.create_sharpe_ratio(equity_df["returns"], self.periods)
        statistics["drawdowns"] = dd_s
        statistics["max_drawdown"] = max_dd
        statistics["max_drawdown_pct"] = max_dd
        statistics["max_drawdown_duration"] = dd_dur
        statistics["equity"] = equity_df["total"]
        statistics["returns"] = equity_df["returns"]
        statistics["cum_returns"] = equity_df["cum_returns"]
        return statistics

    def plot_results(self, filename):
        
        stats = self.get_results(self.port.get_equity_curve())
        
        df = pd.DataFrame(self.port.bars.get_latest_bars(self.port.bars.universe.symbol_list[0],
                                                         self.port.bars.timeframe_list[0], n=100000),
                          columns=["symbol", "datetime", "open", "low", "high", "close", "volume", "candle_opentime"])
        
        df["datetime"] = pd.to_datetime(df["datetime"], unit="s")

        # Creates the Figure
        fig = make_subplots(rows=3, cols=2, subplot_titles=("Price", "Monthly Returns",
                                                            "Equity", "Yearly Returns", "Drawdown", "Statistics"))

        # Creates the layout of the plots
        layout = go.Layout({
            'title': {
                'text': df.symbol[df.first_valid_index()],
                'font': {
                    'size': 15
                }
            }
        })
        # Creates the first trace which plots the price with candlesticks
        trace1 = Plot.plot_price(df)
        # Creates the third trace which plots the Equity
        trace3 = Plot.plot_equity(df, stats)
        # Creates the fifth trace which plots the Drawdown
        trace5 = Plot.plot_drawdown(df, stats)

        fig.add_trace(
            go.Scatter(x=[1, 2, 3], y=[4, 5, 6]),
            row=1, col=2
        )

        fig.add_trace(trace1, row=1, col=1)

        fig.add_trace(trace3, row=2, col=1)

        fig.add_trace(trace5, row=3, col=1)

        fig.update_layout(layout)
        
        fig.update_xaxes(row=1, col=1, rangeslider_visible=False)

        # Create Figure and plot
        if filename is not None:
            fig.write_html(filename)

        fig.show()
