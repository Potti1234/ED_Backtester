import Statistics.Plotting_Plotly as Plot
from Statistics.Statistics import Statistics

from datetime import datetime

import plotly.graph_objects as go
from plotly.subplots import make_subplots


class EntryChartPlotly(Statistics):
    """
    Displays a Candlestick Chart with Entry and Exit Points.
    """

    def __init__(self, df, symbol, portfolio_benchmark=None, title=None, periods=252):
        self.bars = df[0]
        self.returns = df[1]
        self.trades = df[2]
        self.indicators = df[3]
        self.indicators_no = len(df[3])
        self.symbol = symbol
        self.port_bench = portfolio_benchmark
        self.title = title
        self.periods = periods

        # Only use the relevant part of the price data
        self.bars = self.bars[self.bars["datetime"] >= self.returns["datetime"][0]]
        self.bars = self.bars[self.bars["datetime"] <= self.returns["datetime"][self.returns.last_valid_index()]]

    def plot_results(self, filename):

        def ts_to_dt(timestamp):
            return datetime.fromtimestamp(timestamp)

        self.bars["quarter"] = self.bars["datetime"] - (self.bars["datetime"] % (365 * 24 * 60 * 60 / 4))

        dfgb = self.bars.groupby("quarter")

        for name, frame in dfgb:

            frame["datetime"] = frame["datetime"].apply(ts_to_dt)

            # Creates the layout of the plots
            layout = go.Layout({
                'title': {
                    'text': self.symbol,
                    'font': {
                        'size': 15
                    }
                }
            })

            self.trades["datetime"] = self.trades["datetime"].apply(ts_to_dt)

            trace_chart = Plot.plot_price_with_entries(frame, self.trades)

            if self.indicators_no == 0:
                fig = go.Figure(data=trace_chart, layout=layout)
            else:
                subplots = 0
                subplot_traces = []
                for i in self.indicators:
                    if i[1] == "Line_chart":
                        i[0]["datetime"] = i[0]["datetime"].apply(ts_to_dt)
                        trace = Plot.plot_scatter_lines(i[3], i[0]["datetime"], i[0]["0"])
                    else:
                        trace = None
                    if i[2] == "Sub_Plot":
                        subplot_traces.append(trace)
                        subplots += 1
                    else:
                        trace_chart.append(trace)
                if subplots != 0:
                    fig = make_subplots(rows=subplots + 1, cols=1, subplot_titles=("Price", "Indicator1"))
                    for lenght in range(len(trace_chart)):
                        fig.add_trace(trace_chart[lenght], row=1, col=1)
                    for i in range(subplots):
                        fig.add_trace(subplot_traces[i], row=2 + i, col=1)
                else:
                    fig = go.Figure(data=trace_chart, layout=layout)

            # Create Figure and plot
            if filename is not None:
                fig.write_html(filename+"\\"+str(int(name)) + ".html")

            fig.show()
