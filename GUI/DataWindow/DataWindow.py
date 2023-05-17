from PyQt5.QtWidgets import *
from os import listdir
from os.path import isfile, join
import pandas as pd
from GUI.DataWindow.RefactorWindow import RefactorWindow


class DataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.dataDirectory = "D:\\AktienDaten"
        self.dataStatsDirectory = self.dataDirectory + "\\SavedDataStats.csv"
        self.timeframeList = ["1minute", "5minute", "15minute", "30minute", "1hour", "4hour"]#, "1day"]
        self.symbolList = []
        self.dataStats = pd.DataFrame
        self.loadSavedDataStats()

        self.layout = QVBoxLayout()

        self.symbolLayout = QHBoxLayout()
        self.symbolBox = QComboBox()
        self.timeframeBox = QComboBox()

        self.refactorWindow = RefactorWindow(self)
        self.refactorButton = QPushButton()

        self.refreshDataButton = QPushButton()

        self.setWindowTitle("Data")
        self.initLayout()

    def initLayout(self):
        self.initSymbolLayout()
        self.initRefactorButton()
        self.initRefreshDataButton()
        self.layout.addLayout(self.symbolLayout)
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

    def loadSavedDataStats(self):
        self.dataStats = pd.read_csv(self.dataStatsDirectory)
        self.symbolList = self.dataStats["symbol"].unique()

    def saveDataStats(self):
        timeframeData = []
        symbolData = []
        startDateData = []
        endDateData = []

        for timeframe in self.timeframeList:
            path = self.dataDirectory + "\\" + timeframe
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
