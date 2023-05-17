from Statistics.Main_Statistics import round_nearest
from Statistics.Statistics import Statistics
import matplotlib.pyplot as plt
import ast


class TradestatsBar(Statistics):
    """
    Displays a BarChart for Tradestats
    """

    def __init__(self, df, filename, variable_list='[["RRRPercentdifferenceTP", 0.1], ["RRRdifferenceTP", 0.1], '
                                                   '["Profit", 0.5], ["RRR", 0.5], ["stoplosssize", 10], '
                                                   '["Trend", 1], ["commission", 10]]',
                 cummulative=False, descending=False):
        self.bars = df[0]
        self.returns = df[1]
        self.trades = df[2]
        self.indicators = df[3]
        self.indicators_no = len(df[3])
        self.filename = filename
        self.variable_list = variable_list
        if type(variable_list) != "List":
            self.variable_list = ast.literal_eval(variable_list)
        self.cummulative = cummulative
        self.descending = descending

    def plot_results(self, filename):
        dftrades_save = self.trades.copy()

        # Unfinished Code to use more than one variable
        # variable_list = [variable, round_value, cummulative, descending]
        # Save names of variables to groupby and round the values if necessary test
        variables = []
        variable_name = ""
        for variable in self.variable_list:
            variables.append(variable[0])
            variable_name += str(variable[0])
            if variable[1] is not None:
                dftrades_save[variable[0]] = dftrades_save[variable[0]].apply(round_nearest, args=(variable[1],))

        # Group variable and plot wins and losses of every group
        fig, ax = plt.subplots(figsize=(10, 4))
        if self.descending is True:
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
            if len(self.variable_list) != 1:
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
            if self.cummulative is True:
                cumwin[param] += win[param]
                cumloss[param] += loss[param]
                win[param] = cumwin[param]
                loss[param] = cumloss[param]
            # Plot win and loss bars
            ax.bar(grp[variables[0]][grp.first_valid_index()], win[param], width=self.variable_list[0][1] / 2, color="green",
                   align="edge")
            ax.bar(grp[variables[0]][grp.first_valid_index()], loss[param], width=-self.variable_list[0][1] / 2, color="red",
                   align="edge")

        plt.savefig("D:\\AktienDaten\\Statistics\\{} WinnerLoser.png".format(filename))

        fig, ax = plt.subplots(figsize=(10, 4))
        for key, grp in dfgb:
            variable_value = ""
            param = grp.first_valid_index()
            if len(self.variable_list) != 1:
                for i in key:
                    variable_value += str(i)
                param = variable_value
            profit[param] = grp["Profit"].sum()
            if self.cummulative is True:
                cumprofit[param] += profit[param]
                profit[param] = cumprofit[param]
            ax.bar(grp[variables[0]][grp.first_valid_index()], profit[param], width=self.variable_list[0][1], color="green")
        plt.savefig("D:\\AktienDaten\\Statistics\\{} Profit.png".format(filename))

        for key, grp in dfgb:
            variable_value = ""
            param = grp.first_valid_index()
            if len(self.variable_list) != 1:
                for i in key:
                    variable_value += str(i)
                param = variable_value

            with open("D:\\AktienDaten\\Statistics\\{} {}.txt".format(filename, variable_name), 'a') as f:
                f.write('{} {}W {}L {}% {}Profit\n'.format(param, win[param], loss[param],
                                                           round(win[param] / (win[param] + loss[param]), 2),
                                                           round(profit[param]), 2))
                f.close()
