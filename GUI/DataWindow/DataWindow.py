from datetime import datetime
from PyQt5.QtWidgets import *
from os import listdir
from os.path import isfile, join
import pandas as pd
from GUI.DataWindow.RefactorWindow import RefactorWindow
import Constants
import Statistics.Plotting_Bokeh as Plot
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column


class DataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.dataDirectory = Constants.DATA_DIRECTORY
        self.dataStatsDirectory = Constants.DATA_DIRECTORY + "SavedDataStats.csv"
        self.timeframeList = ["1minute", "5minute", "15minute", "30minute", "1hour", "4hour"]#, "1day"]
        self.symbolList = []
        self.dataStats = pd.DataFrame
        self.loadSavedDataStats()

        self.layout = QVBoxLayout()

        self.symbolLayout = QHBoxLayout()
        self.symbolBox = QComboBox()
        self.timeframeBox = QComboBox()

        self.statisticsLayout = QHBoxLayout()
        self.plotChartButton = QPushButton()
        self.startDateTextField = QLineEdit()
        self.endDateTextField = QLineEdit()

        self.refactorWindow = RefactorWindow(self)
        self.refactorButton = QPushButton()

        self.refreshDataButton = QPushButton()

        self.setWindowTitle("Data")
        self.initLayout()

    def initLayout(self):
        self.initSymbolLayout()
        self.initStatisticsLayout()
        self.initRefactorButton()
        self.initRefreshDataButton()
        self.layout.addLayout(self.symbolLayout)
        self.layout.addLayout(self.statisticsLayout)
        self.layout.addWidget(self.refactorButton)
        self.layout.addWidget(self.refreshDataButton)
        self.setLayout(self.layout)

    def initRefreshDataButton(self):
        self.refreshDataButton.setText("refresh Data")
        self.refreshDataButton.clicked.connect(self.refreshDataButtonClicked)

    def refreshDataButtonClicked(self):
        self.saveDataStats()

    def initRefactorButton(self):
        self.refactorButton.setText("refactor")
        self.refactorButton.clicked.connect(self.refactorButtonClicked)

    def refactorButtonClicked(self):
        self.refactorWindow.show()

    def initSymbolLayout(self):
        self.initSymbolBox()
        self.initTimeframeBox()

        self.symbolLayout.addWidget(self.symbolBox)
        self.symbolLayout.addWidget(self.timeframeBox)

    def initSymbolBox(self):
        self.symbolBox.setToolTip("Symbol")
        self.symbolBox.addItems(self.symbolList)
        self.symbolBox.setEditable(True)
        self.symbolBox.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.symbolBox.currentTextChanged.connect(self.symbolBoxChanged)

    def initTimeframeBox(self):
        self.timeframeBox.setToolTip("Timeframe")
        self.timeframeBox.setEditable(True)
        self.timeframeBox.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.symbolBoxChanged()

    def symbolBoxChanged(self):
        symbolStats = self.dataStats[self.dataStats["symbol"] == self.symbolBox.currentText()]
        self.timeframeBox.clear()
        self.timeframeBox.addItems(symbolStats["timeframe"].unique())
        self.refactorWindow.symbolText.setText(self.symbolBox.currentText())
        self.refactorWindow.initRefactorBox()

        self.startDateTextField.setText(str(ts_to_dt(symbolStats["startDate"].min())))
        self.endDateTextField.setText(str(ts_to_dt(symbolStats["endDate"].max())))

    def initStatisticsLayout(self):
        self.plotChartButton.setText("Plot Chart")
        self.plotChartButton.clicked.connect(self.plotPrice)

        self.startDateTextField.setToolTip("StartDate")
        self.endDateTextField.setToolTip("EndDate")
        self.startDateTextField.setEnabled(False)
        self.endDateTextField.setEnabled(False)

        self.statisticsLayout.addWidget(self.plotChartButton)
        self.statisticsLayout.addWidget(self.startDateTextField)
        self.statisticsLayout.addWidget(self.endDateTextField)

    def loadSavedDataStats(self):
        self.dataStats = pd.read_csv(self.dataStatsDirectory)
        self.symbolList = self.dataStats["symbol"].unique()

    def saveDataStats(self):
        timeframeData = []
        symbolData = []
        startDateData = []
        endDateData = []

        for timeframe in self.timeframeList:
            path = self.dataDirectory + timeframe
            # Get all files in timeframe folder
            files = [f for f in listdir(path) if isfile(join(path, f))]
            for file in files:
                if ".csv" not in file:
                    continue
                fileData = pd.read_csv(join(path, file))
                timeframeData.append(timeframe)
                symbolData.append(file.replace(".csv", ""))
                startDateData.append(fileData["datetime"][fileData.first_valid_index()])
                endDateData.append(fileData["datetime"][fileData.last_valid_index()])

        dataStats = pd.DataFrame({"timeframe": timeframeData, "symbol": symbolData, "startDate": startDateData,
                                  "endDate": endDateData})
        dataStats.to_csv(self.dataStatsDirectory)

    def plotPrice(self):
        df = pd.read_csv(Constants.DATA_DIRECTORY + self.timeframeBox.currentText() + "\\" +
                         self.symbolBox.currentText() + ".csv")

        df["datetime"] = df["datetime"].apply(ts_to_dt)

        tools = "pan,wheel_zoom,ywheel_zoom,xwheel_zoom,box_zoom,reset,save"

        figures = [figure(x_axis_type="datetime", tools=tools, plot_width=1500, plot_height=500, title="Chart")]

        figures[0] = Plot.add_price(figures[0], df)

        output_file(Constants.DATA_DIRECTORY + "PriceChart.html", title="PriceChart.html")

        show(column(*figures))


def ts_to_dt(timestamp):
    try:
        return datetime.fromtimestamp(int(timestamp))
    except ValueError or TypeError:
        return timestamp
