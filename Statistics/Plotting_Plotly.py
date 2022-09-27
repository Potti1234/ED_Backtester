def plot_price_with_entries(df, trades):
    buys = trades[trades["size"] >= 0]
    sells = trades[trades["size"] <= 0]

    trace1 = {
        'x': df.datetime,
        'open': df.open,
        'close': df.close,
        'high': df.high,
        'low': df.low,
        'type': 'candlestick',
        'name': "Chart",
        'showlegend': False
    }
    trace2 = {
        'x': buys.datetime,
        'y': buys.price,
        'type': 'scatter',
        'mode': 'markers',
        'line': {
            'width': 10,
            'color': 'blue'
        },
        'name': 'BUY'
    }
    trace3 = {
        'x': sells.datetime,
        'y': sells.price,
        'type': 'scatter',
        'mode': 'markers',
        'line': {
            'width': 10,
            'color': 'orange'
        },
        'name': 'SELL'
    }
    trace = [trace1, trace2, trace3]
    return trace


def plot_price(df):
    trace = {
        'x': df.datetime,
        'open': df.open,
        'close': df.close,
        'high': df.high,
        'low': df.low,
        'type': 'candlestick',
        'name': "Chart",
        'showlegend': False
    }
    return trace


def plot_equity(df, stats):
    trace = {
        'x': df.datetime,
        'y': stats["cum_returns"],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'Equity'
    }
    return trace


def plot_drawdown(df, stats):
    trace = {
        'x': df.datetime,
        'y': -100 * stats["drawdowns"],
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': 'Drawdown'
    }
    return trace


def plot_scatter_lines(name, xaxis, yaxis):
    trace = {
        'x': xaxis,
        'y': yaxis,
        'type': 'scatter',
        'mode': 'lines',
        'line': {
            'width': 1,
            'color': 'blue'
        },
        'name': name
    }
    return trace
