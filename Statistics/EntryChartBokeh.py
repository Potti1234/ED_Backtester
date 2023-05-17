import Statistics.Plotting_Bokeh as Plot
from Statistics.Statistics import Statistics

from datetime import datetime

from bokeh.plotting import output_file, figure, save
from bokeh.layouts import column


class EntryChartBokeh(Statistics):
    """
    Displays a Candlestick Chart with Entry and Exit Points.
    """

    def __init__(self, df, symbol, portfolio_benchmark=None, title=None, plot_sltp=False):
        self.bars = [d[0][0] for d in df]
        self.bars_tf = [d[0][1] for d in df]
        self.returns = df[0][1]
        self.trades = df[0][2]
        self.indicators = df[0][3]
        self.indicators_no = len(df[0][3])
        self.symbol = symbol
        self.port_bench = portfolio_benchmark
        self.title = title
        self.plot_sltp = plot_sltp

    def plot_results(self, filename):

        def ts_to_dt(timestamp):
            try:
                return datetime.fromtimestamp(int(timestamp))
            except TypeError:
                return timestamp

        figures = []
        tools = "pan,wheel_zoom,ywheel_zoom,xwheel_zoom,box_zoom,reset,save"

        self.trades["datetime"] = self.trades["datetime"].apply(ts_to_dt)
        self.returns["datetime"] = self.returns["datetime"].apply(ts_to_dt)

        plotnr = 0
        for bars in self.bars:
            bars["datetime"] = bars["datetime"].apply(ts_to_dt)
            figures.append(figure(x_axis_type="datetime", tools=tools, plot_width=1500, plot_height=500, title="Chart"))
            figures[plotnr] = Plot.add_price(figures[plotnr], bars)
            figures[plotnr] = Plot.add_entries(figures[plotnr], self.trades)
            if self.plot_sltp is True:
                figures[plotnr] = Plot.add_sltp(figures[plotnr], self.trades)
            plotnr += 1

        figures.append(figure(x_axis_type="datetime", x_range=figures[0].x_range, tools=tools,
                              plot_width=1500, plot_height=250, title="Return"))
        figures[plotnr] = Plot.add_scatter_lines(figures[plotnr], "Return", self.returns["datetime"],
                                                 self.returns["total"])

        if self.indicators_no != 0:
            for i in self.indicators:
                i[0]["datetime"] = i[0]["datetime"].apply(ts_to_dt)
                figures_number = 0
                if i[2] == "Sub_Plot":
                    figures.append(figure(x_axis_type="datetime", x_range=figures[0].x_range, tools=tools,
                                          plot_width=1500, plot_height=250, title=i[3]))
                    figures_number = -1
                for f in range(len(self.bars)):
                    if self.bars_tf[f] == i[4] or figures_number == -1:
                        if i[1] == "Line_chart":
                            figures[figures_number] = Plot.add_scatter_lines(figures[figures_number], i[3],
                                                                             i[0]["datetime"], i[0]["0"], color=i[5])
                        elif i[1] == "Two_Line_chart":
                            figures[figures_number] = Plot.add_scatter_lines(figures[figures_number], i[3],
                                                                             i[0]["datetime"], i[0]["0"])
                            figures[figures_number] = Plot.add_scatter_lines(figures[figures_number], i[3],
                                                                             i[0]["datetime"], i[0]["1"], color="red")
                        elif i[1] == "Line_chart_plus_lines":
                            figures[figures_number] = Plot.add_scatter_lines(figures[figures_number], i[3],
                                                                             i[0]["datetime"], i[0]["0"])
                            for line_value in i[5]:
                                y = [line_value] * len(i[0])
                                figures[figures_number] = Plot.add_scatter_lines(figures[figures_number], i[3],
                                                                                 i[0]["datetime"], y, color="red")
                    if figures_number == -1:
                        break
                    else:
                        figures_number += 1

        # Create Figure and plot
        if filename is not None:
            output_file(filename+"\\"+str(self.title) + ".html", title=filename+"\\"+str(self.title) + ".html")

        save(column(*figures))
