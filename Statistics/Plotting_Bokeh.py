def add_price(edit_figure, df):
    inc = df.close > df.open
    dec = df.open > df.close

    index_values = df.index.values
    first = df["datetime"][index_values[0]]
    second = df["datetime"][index_values[1]]

    width = (second - first) / 2

    edit_figure.segment(df.datetime, df.high, df.datetime, df.low, color="black")
    edit_figure.vbar(df.datetime[inc], width, df.open[inc], df.close[inc], fill_color="#4ED42C", line_color="black")
    edit_figure.vbar(df.datetime[dec], width, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")

    return edit_figure


def add_entries(edit_figure, trades):
    buys = trades[trades["size"] >= 0]
    sells = trades[trades["size"] <= 0]

    edit_figure.circle(buys.datetime, buys.price, size=8, color="blue")
    edit_figure.circle(sells.datetime, sells.price, size=8, color="red")

    return edit_figure


def add_sltp(edit_figure, trades):
    trades = trades.dropna()

    edit_figure.circle(trades.datetime, trades.stop_loss, size=8, color="yellow")
    edit_figure.circle(trades.datetime, trades.take_profit, size=8, color="green")

    return edit_figure


def add_scatter_lines(edit_figure, name, xaxis, yaxis, color="blue"):
    edit_figure.line(xaxis, yaxis, legend_label=name, line_width=2, line_color=color)
    return edit_figure
