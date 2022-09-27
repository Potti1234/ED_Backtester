import quantstats as qs
from ED_Backtester.Statistics.statistics import Statistics
import pandas as pd


class Tearsheet_quantstats(Statistics):
    """
    Displays a Plotly-generated 'one-pager' as often
    found in institutional strategy performance reports.
    """

    def __init__(self, df, portfolio_benchmark=None, title=None):
        self.df = df
        self.port_bench = portfolio_benchmark
        self.title = title

    def plot_results(self, filename):
        #df = self.df["datetime"]
        #df = pd.to_datetime(df, unit="s")
        #stats = pd.Series(data=self.df["total"].pct_change(), index=self.df["datetime"])
        #stats.index = df
        df = self.df
        df["datetime"] = pd.to_datetime(df["datetime"], unit="s")
        df.index = df["datetime"]
        df["total"] = df["total"].pct_change()
        stats = df["total"].squeeze()
        print(self.df)
        print(stats)
        if filename is not None:
            qs.reports.html(stats, self.port_bench, output=filename, download_filename=filename)
            #qs.reports.basic(stats, self.port_bench)
        else:
            print("You need to enter a filename")
