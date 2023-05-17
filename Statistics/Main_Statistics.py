import pandas as pd
import numpy as np
from datetime import datetime
import time
from decimal import Decimal
import matplotlib.pyplot as plt

from Statistics.EntryChartBokeh import EntryChartBokeh
from Statistics.Tearsheet_quantstats import Tearsheet_quantstats

import Statistics.Indicator_lists as Indicator_lists
import Symbol_lists as Symbol_lists


def reformat_data(rf_data, reformat_data_sec, base_data_sec):
    rf_data["candle_opentime"] = rf_data["datetime"] - (rf_data["datetime"] % reformat_data_sec)
    rf_data["is last candle"] = rf_data["candle_opentime"] + reformat_data_sec - base_data_sec
    rf_data = rf_data[rf_data["datetime"] == rf_data["is last candle"]]
    return rf_data


def main():
    symbol_list = Symbol_lists.return_forexpairs()
    # symbol_list = ["EURUSD"]
    # symbol_list = ["ES"]

    indicator_list = [["EMA", "Line_chart", "Main_Plot", "EMA"],
                      ["MajorSwingLevels", "Line_chart", "Main_Plot", "MajorSwingLevels"],
                      ["Hidden_Divergence", "Line_chart", "Sub_Plot", "Hidden_Divergence"],
                      ["RSI", "Line_chart_plus_lines", "Sub_Plot", "RSI", [50, 50]],
                      ["Stochastic", "Two_Line_chart", "Sub_Plot", "Stochastic"],
                      ["MACD", "Two_Line_chart", "Sub_Plot", "MACD"]]
    # indicator_list = Indicator_lists.return_MSLReversalIndicators()
    indicator_list = Indicator_lists.return_MSLBreakoutIndicators()
    start_date = "2019/01/01 00:00:00"
    start_date = time.mktime(datetime.strptime(start_date, '%Y/%m/%d %H:%M:%S').timetuple())
    end_date = "2023/01/01 00:00:00"
    end_date = time.mktime(datetime.strptime(end_date, '%Y/%m/%d %H:%M:%S').timetuple())
    #plot_entry_chart("MSLTest", "EURUSD", ["15minute", "4hour"], 2, "MSLTestSLTP", start_date, end_date, indicator_list, 900, plot_slpt=True)
    # for symbol in symbol_list:
    #     plot_entry_chart("MSLReversalReversed", symbol, ["15minute", "4hour"], 2, "MSLReversalChart15minReversed2", start_date, end_date, indicator_list, 900)
    plot_tearsheet("MSLBreakout", "TearsheetAllTrades")
    # plot_single_trades("MSL", "EURUSD", ["15minute", "4hour"], 0, indicator_list, 14400, prev_bars=100, after_bars=10)
    parameters = [[["RRRPercentdifferenceTP", 0.1]], [["RRRdifferenceTP", 0.1]], [["Profit", 0.5]], [["RRR", 0.5]],
                  [["stoplosssize", 10]], [["Trend", 1]], [["commission", 10]]]
    #parameters = [[["Range_Filter25", 10]], [["Range_Filter50", 10]], [["Range_Filter75", 10]], [["Range_Filter100", 10]], [["Range_Filter200", 10]]]
    #parameters = [[["Range_Filter200", 10], ["Direction", None]]]
    tp_sl_optimize = True
    #for p in parameters:
     #   plot_trades_analysis("MSLBreakout", symbol_list, "15minute", indicator_list, p, tp_sl_optimize, tp_sl_optimize)
      #  tp_sl_optimize = False
    #plot_entry_chart("MSLBreakout", "EURUSD", ["15minute", "4hour"], 0, "MSLBreakout", start_date, end_date, indicator_list,
     #                900, plot_slpt=True)


def load_data(strategy_name, symbol, timeframe, indicator_list):
    statistics_filename = "D:\\AktienDaten\\Statistics\\{}\\{}\\".format(strategy_name, symbol)
    statistics_main_filename = "D:\\AktienDaten\\Statistics\\{}\\".format(strategy_name)

    df = []
    try:
        df.append([pd.read_csv("D:\\AktienDaten\\{}\\{}.csv".format(timeframe, symbol)), timeframe])
    except FileNotFoundError:
        df_base = pd.read_csv("D:\\AktienDaten\\1minute\\{}.csv".format(symbol))
        df_base["candle_opentime"] = df_base["datetime"] - (df_base["datetime"] % get_timeframe_in_sec(timeframe))
        # Transform Data into lowest timeframe format
        dfgb = df_base.groupby("candle_opentime")

        df_hilf = pd.DataFrame()
        df_hilf["datetime"] = dfgb["datetime"].first()
        df_hilf["open"] = dfgb["open"].first()
        df_hilf["low"] = dfgb["low"].min()
        df_hilf["high"] = dfgb["high"].max()
        df_hilf["close"] = dfgb["close"].last()
        df_hilf["volume"] = dfgb["volume"].sum()
        df_hilf.reset_index()
        df.append([df_hilf, timeframe])
    df.append(pd.read_csv(statistics_main_filename + "Return.csv"))
    df.append(pd.read_csv(statistics_filename + "Trades.csv"))

    indicators = []
    for indicator in indicator_list:
        ind = [pd.read_csv(statistics_filename + indicator[0] + ".csv")]
        for i in range(1, len(indicator)):
            ind.append(indicator[i])
        indicators.append(ind)

    df.append(indicators)
    return df


def get_timeframe_in_sec(timeframe):
    """
    Convert the string timeframe int a int value
    Args:
        timeframe: the timeframe to convert

    Returns:
        int: seconds of the timeframe
    """
    seconds = 0
    if "minute" in timeframe:
        seconds = 60
        timeframe = timeframe.replace("minute", "")
    elif "hour" in timeframe:
        seconds = 60 * 60
        timeframe = timeframe.replace("hour", "")
    elif "day" in timeframe:
        seconds = 60 * 60 * 24
        timeframe = timeframe.replace("day", "")

    return seconds * int(timeframe)


def plot_entry_chart(strategy_name, symbol, timeframe_list, drop_candles, title, start_date, end_date, indicator_list,
                     reformat_data_sec=0, plot_slpt=False, trades=None):
    statistics_filename = "D:\\AktienDaten\\Statistics\\{}\\{}\\".format(strategy_name, symbol)

    full_df = []

    for timeframe in timeframe_list:
        df = load_data(strategy_name, symbol, timeframe, indicator_list)

        if trades is not None:
            df[2] = trades

        for indicator in df[3]:
            indicator[0] = indicator[0].iloc[drop_candles:, :]

        if reformat_data_sec != 0:
            for i in range(2):
                reformat_data_sec = get_timeframe_in_sec(timeframe)
                if i == 0:
                    df[i][0] = reformat_data(df[i][0], reformat_data_sec, 60)
                else:
                    df[i] = reformat_data(df[i], reformat_data_sec, get_timeframe_in_sec(timeframe_list[0]))
        # Only use the relevant part of the price data
        price = df[0][0]
        price = price[price.datetime >= df[1].datetime[df[1].first_valid_index()]]
        price = price[price.datetime <= df[1].datetime[df[1].last_valid_index()]]
        price = price.iloc[drop_candles:, :]
        df[0][0] = price

        for i in range(3):
            if i == 0:
                df[i][0] = df[i][0][df[i][0].datetime >= start_date]
                df[i][0] = df[i][0][df[i][0].datetime <= end_date]
            else:
                df[i] = df[i][df[i].datetime >= start_date]
                df[i] = df[i][df[i].datetime <= end_date]
        for indicator in df[3]:
            indicator[0] = indicator[0][indicator[0].datetime >= start_date]
            indicator[0] = indicator[0][indicator[0].datetime <= end_date]

        full_df.append(df)

    statistics = EntryChartBokeh(full_df, symbol, title=title, plot_sltp=plot_slpt)
    statistics.plot_results(statistics_filename)


def plot_tearsheet(strategy_name, title, symbol=None):
    statistics_filename = "D:\\AktienDaten\\Statistics\\{}\\".format(strategy_name)
    if symbol is not None:
        statistics_filename += symbol + "\\"

    df = pd.read_csv(statistics_filename + "Return.csv")

    statistics = Tearsheet_quantstats(df)
    statistics.plot_results(statistics_filename + title + ".html")


def plot_single_trades(strategy_name, symbol, timeframe, drop_candles, indicator_list, reformat_data_sec=0,
                       prev_bars=40, after_bars=10):
    statistics_filename = "D:\\AktienDaten\\Statistics\\{}\\{}\\".format(strategy_name, symbol)

    trades = pd.read_csv(statistics_filename + "Trades.csv")
    open_trades = trades[trades["OC"] == "Open"]
    close_trades = trades[trades["OC"] == "Close"]

    open_dt = open_trades["datetime"].values
    close_dt = close_trades["datetime"].values

    for i in range(len(close_dt)):
        trades = open_trades.iloc[[i]]
        trades = trades.append(close_trades.iloc[[i]])

        plot_entry_chart(strategy_name, symbol, timeframe, drop_candles, "Trades\\" + str(i), open_dt[i] - prev_bars *
                         reformat_data_sec, close_dt[i] + after_bars * reformat_data_sec, indicator_list,
                         reformat_data_sec, True, trades)


def round_nearest(num, to):
    num, to = Decimal(str(num)), Decimal(str(to))
    try:
        return float(round(num / to) * to)
    except OverflowError:
        return num


def plot_tradestats_bar(dftrades, filename, variable_list, cummulative=False, descending=False):
    dftrades_save = dftrades.copy()

    # Unfinished Code to use more than one variable
    # variable_list = [variable, round_value, cummulative, descending] 
    # Save names of variables to groupby and round the values if necessary
    variables = []
    variable_name = ""
    for variable in variable_list:
        variables.append(variable[0])
        variable_name += str(variable[0])
        if variable[1] is not None:
            dftrades_save[variable[0]] = dftrades_save[variable[0]].apply(round_nearest, args=(variable[1],))

    # Group variable and plot wins and losses of every group
    fig, ax = plt.subplots(figsize=(10, 4))
    if descending is True:
        dfgb = dftrades_save.iloc[::-1].groupby(variables)
    else:
        dfgb = dftrades_save.groupby(variables)
    # Initialise stats variables
    win = {}
    loss = {}
    profit = {}
    # Initialise cummulative variables
    cumwin = {}
    cumloss = {}
    cumprofit = {}
    for key, grp in dfgb:
        variable_value = ""
        param = grp.first_valid_index()
        # Combine current key values to one string if more than one variable is used
        if len(variable_list) != 1:
            for i in key:
                variable_value += str(i)
            param = variable_value
        # Calculate wins and losses of current group
        try:
            win[param] = grp["WL"].value_counts()["Win"]
        except KeyError:
            win[param] = 0
        try:
            loss[param] = grp["WL"].value_counts()["Loss"]
        except KeyError:
            loss[param] = 0
        # Calculate cumulative wins and losses
        if cummulative is True:
            cumwin[param] += win[param]
            cumloss[param] += loss[param]
            win[param] = cumwin[param]
            loss[param] = cumloss[param]
        # Plot win and loss bars
        ax.bar(grp[variables[0]][grp.first_valid_index()], win[param], width=variable_list[0][1] / 2, color="green",
               align="edge")
        ax.bar(grp[variables[0]][grp.first_valid_index()], loss[param], width=-variable_list[0][1] / 2, color="red",
               align="edge")

    plt.savefig("D:\\AktienDaten\\Statistics\\{} WinnerLoser.png".format(filename))

    fig, ax = plt.subplots(figsize=(10, 4))
    for key, grp in dfgb:
        variable_value = ""
        param = grp.first_valid_index()
        if len(variable_list) != 1:
            for i in key:
                variable_value += str(i)
            param = variable_value
        profit[param] = grp["Profit"].sum()
        if cummulative is True:
            cumprofit[param] += profit[param]
            profit[param] = cumprofit[param]
        ax.bar(grp[variables[0]][grp.first_valid_index()], profit[param], width=variable_list[0][1], color="green")
    plt.savefig("D:\\AktienDaten\\Statistics\\{} Profit.png".format(filename))

    for key, grp in dfgb:
        variable_value = ""
        param = grp.first_valid_index()
        if len(variable_list) != 1:
            for i in key:
                variable_value += str(i)
            param = variable_value

        with open("D:\\AktienDaten\\Statistics\\{} {}.txt".format(filename, variable_name), 'a') as f:
            f.write('{} {}W {}L {}% {}Profit\n'.format(param, win[param], loss[param],
                                                       round(win[param] / (win[param] + loss[param]), 2),
                                                       round(profit[param]), 2))
            f.close()


def plot_tradestats_scatter(dftrades, filename, variable):
    fig = plt.figure()
    colors = {'Win': 'green', 'Loss': 'red'}
    plt.scatter(dftrades.index, dftrades[variable], c=dftrades["WL"].map(colors))
    plt.savefig("D:\\AktienDaten\\Statistics\\{} Scatter.png".format(filename))


def save_stats(trades, symbol, statistics_filename):
    try:
        win = trades["WL"].value_counts()["Win"]
    except KeyError:
        win = 0
    loss = trades["WL"].value_counts()["Loss"]
    winrate = round(win / (win + loss), 2)
    profit = round(trades["Profit"].sum(), 2)

    with open(statistics_filename + 'Sum.txt', 'a') as f:
        f.write('{} {}W {}L {}% {}Profit\n'.format(symbol, win, loss, winrate, profit))
        f.close()


def plot_trades_analysis(strategy_name, symbol_list, timeframe, indicator_list, variable_list, tp_optimization=True,
                         sl_optimization=True):
    alltrades = pd.DataFrame()
    # Give Name of value to plot on x axis and digits to round plot winrate trades profit
    statistics_filename = "D:\\AktienDaten\\Statistics\\{}\\".format(strategy_name)
    variable_name = ""
    for variable in variable_list:
        variable_name += str(variable[0])
    for symbol in symbol_list:
        dftrades = trade_analysis(strategy_name, symbol, timeframe, indicator_list)
        # Filter commissions over 100
        dftrades = dftrades.loc[dftrades['commission'] < 100]

        # Save stats in Sum.txt file
        save_stats(dftrades, symbol, statistics_filename)

        alltrades = alltrades.append(dftrades, ignore_index=True)

        plot_tradestats_bar(dftrades, "{}\\{}\\{}".format(strategy_name, symbol, variable_name), variable_list)
        for variable in variable_list:
            plot_tradestats_scatter(dftrades, "{}\\{}\\{}".format(strategy_name, symbol, variable[0]), variable[0])

    # Calculate Cummulative Profit to use for the modelling of a profit graph
    alltrades["CumProfit"] = alltrades["Profit"].cumsum()
    alltrades["CommissionCumProfit"] = alltrades["CommissionProfit"].cumsum()
    # print(sum(alltrades["CommissionProfit"]))
    # print(sum(alltrades["Profit"]))

    # Optimize TP and sl placement if activated
    if tp_optimization is True:
        best_price_profits(alltrades, "RRRPercentdifferenceTP", alltrades["RRR"],
                           statistics_filename=statistics_filename)
    if sl_optimization is True:
        best_price_profits(alltrades, "RRRPercentdifferenceSL", alltrades["RRR"], 1,
                           statistics_filename=statistics_filename)

    save_stats(alltrades, "All   ", statistics_filename)
    plot_tradestats_bar(alltrades, "{}\\{}".format(strategy_name, variable_name), variable_list)
    for variable in variable_list:
        plot_tradestats_scatter(alltrades, "{}\\{}".format(strategy_name, variable[0]), variable[0])


def trade_analysis(strategy_name, symbol, timeframe, indicator_list):
    df = load_data(strategy_name, symbol, timeframe, indicator_list)

    trades = df[2]
    trades = trades.drop("Unnamed: 0", axis=1)

    dftrades = pd.DataFrame()
    # Match open and close trades
    save_row = 0
    for index, row in trades.iterrows():
        if row["OC"] == "Open":
            save_row = row
        elif row["OC"] == "Close":
            if save_row["size"] + row["size"] != 0:
                save_row["size"] += row["size"]
            save_row["datetimeclose"] = row["datetime"]
            save_row["closeprice"] = row["price"]
            save_row["closesize"] = row["size"]
            # Check Winner or Loser
            if save_row["size"] > 0:
                if save_row["price"] > save_row["closeprice"]:
                    save_row["WL"] = "Loss"
                else:
                    save_row["WL"] = "Win"
            else:
                if save_row["price"] < save_row["closeprice"]:
                    save_row["WL"] = "Loss"
                else:
                    save_row["WL"] = "Win"
            dftrades = dftrades.append(save_row)

    # Check if it is a Buy or Sell trade
    dftrades.loc[dftrades['size'] > 0, 'Direction'] = "Buy"
    dftrades.loc[dftrades['size'] < 0, 'Direction'] = "Sell"

    dftrades["opentime"] = dftrades["datetimeclose"] - dftrades["datetime"]
    # TP = 0 Use Exitprice
    dftrades.loc[dftrades['take_profit'].isnull() == True, 'take_profit'] = dftrades["closeprice"]

    dftrades["stoplosssize"] = abs(dftrades["stop_loss"] - dftrades["price"])
    dftrades["takeprofitsize"] = abs(dftrades["take_profit"] - dftrades["price"])

    dftrades["RRR"] = dftrades["takeprofitsize"] / dftrades["stoplosssize"]
    # Use Best TP Price column
    dftrades["MaxRRRTP"] = abs(dftrades["BestTPPrice"] - dftrades["price"]) / dftrades["stoplosssize"]
    dftrades["RRRdifferenceTP"] = dftrades["MaxRRRTP"] - dftrades["RRR"]
    dftrades["RRRPercentdifferenceTP"] = dftrades["MaxRRRTP"] / dftrades["RRR"]
    # Use Best SL Price column
    dftrades["MaxRRRSL"] = dftrades["takeprofitsize"] / abs(dftrades["BestSLPrice"] - dftrades["price"])
    dftrades["RRRdifferenceSL"] = dftrades["MaxRRRSL"] - dftrades["RRR"]
    dftrades["RRRPercentdifferenceSL"] = dftrades["MaxRRRSL"] / dftrades["RRR"]
    # Calculate Profit Column
    dftrades["Profit"] = dftrades["RRR"]
    dftrades.loc[dftrades['WL'] == "Loss", 'Profit'] = -1
    # Calculate commissions in the Profit and RRR
    dftrades["CommissionRRR"] = dftrades["RRR"] - dftrades["commission"] * 2 / 1000
    dftrades["CommissionProfit"] = dftrades["Profit"] - dftrades["commission"] * 2 / 1000
    dftrades.loc[dftrades['CommissionProfit'] <= 0, 'WL'] = "Loss"
    dftrades.loc[dftrades['CommissionProfit'] > 0, 'WL'] = "Win"
    # Calculate Cummulative Profit to use for the modelling of a profit graph
    dftrades["CumProfit"] = dftrades["Profit"].cumsum()
    dftrades["CommissionCumProfit"] = dftrades["CommissionProfit"].cumsum()

    return dftrades


def best_price_profits(alltrades, mode="MaxRRRTP", factor=1, commission_factor=None, commission_max=100,
                       statistics_filename=None):
    # factor = alltrades["RRR"] with percentage
    # commission_factor = alltrades["RRR"] with MaxRRRSL and 1 with percent
    maxrrr = alltrades[mode].values.round(2)
    maxrrr = list(set(maxrrr))
    maxrrr.sort()
    results = []
    for i in maxrrr:
        alltrades_copy = alltrades.copy()
        # Calculate new profit and loss
        alltrades_copy.loc[alltrades_copy[mode] < i, 'Profit'] = -1
        alltrades_copy.loc[alltrades_copy[mode] >= i, 'Profit'] = factor * i
        # Adjust commissions
        if commission_factor is not None:
            alltrades_copy["commission"] = alltrades_copy["commission"] * i / commission_factor
            alltrades_copy = alltrades_copy.loc[alltrades_copy['commission'] < commission_max]
        # Calculate commission profits
        alltrades_copy["CommissionProfit"] = alltrades_copy["Profit"] - alltrades_copy["commission"] * 2 / 1000
        # Filter out infinity values
        alltrades_copy = alltrades_copy.loc[alltrades_copy[mode] != np.inf]
        # Calculate Cummulative Profit to use for the modelling of a profit graph
        alltrades_copy["CumProfit"] = alltrades_copy["Profit"].cumsum()
        alltrades_copy["CommissionCumProfit"] = alltrades_copy["CommissionProfit"].cumsum()
        # Calculate numbers of winners and losers
        cut = pd.cut(alltrades_copy.Profit, [-np.inf, 0, np.inf], labels=['loss', 'win'])
        wl = pd.value_counts(cut, sort=False).rename_axis('wl').reset_index(name='count')
        wl = wl.values
        win = wl[1][1]
        loss = wl[0][1]
        winrate = 0
        if win+loss != 0:
            winrate = round(win / (win + loss), 2)
        # Save Results
        results.append([i, round(sum(alltrades_copy["Profit"]), 2), round(sum(alltrades_copy["CommissionProfit"]), 2),
                        win, loss, winrate])
        # Print out the results
        print(i, sum(alltrades_copy["CommissionProfit"]), sum(alltrades_copy["Profit"]))
    # Check if data should be saved
    if statistics_filename is None:
        return
    # Save the data in a txt file
    with open(statistics_filename + mode + '.txt', 'a') as f:
        for result in results:
            f.write('{} {} Profit {} CommissionProfit {} Wins {} Losses {} Winrate\n'.format(*result))
        f.close()


if __name__ == "__main__":
    main()
