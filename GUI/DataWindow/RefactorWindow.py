from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread
import HistoricDataLoader


class RefactorWindow(QWidget):
    def __init__(self, dataWindow):
        super().__init__()
        self.dataWindow = dataWindow

        self.layout = QVBoxLayout()

        self.symbolText = QLineEdit()

        self.refactorLayout = QHBoxLayout()
        self.refactorButton = QPushButton()
        self.refactorTimeframeBox = QComboBox()

        self.setWindowTitle("Refactor")
        self.initLayout()

        self.setLayout(self.layout)

    def initLayout(self):
        self.initSymbolText()
        self.initRefactorLayout()

        self.layout.addWidget(self.symbolText)
        self.layout.addLayout(self.refactorLayout)

    def initSymbolText(self):
        self.symbolText.setText(self.dataWindow.symbolBox.currentText())

    def initRefactorLayout(self):
        self.initRefactorButton()
        self.initRefactorBox()

        self.refactorLayout.addWidget(self.refactorButton)
        self.refactorLayout.addWidget(self.refactorTimeframeBox)

    def initRefactorButton(self):
        self.refactorButton.setText("refactor")
        self.refactorButton.clicked.connect(self.refactorButtonClicked)

    def refactorButtonClicked(self):
        self.refactorButton.setEnabled(False)

        data = self.dataWindow.dataStats[self.dataWindow.dataStats["timeframe"] == "1minute"]
        data = data[data["symbol"] == self.dataWindow.symbolBox.currentText()]
        startDate = data["startDate"][data.first_valid_index()]
        endDate = data["endDate"][data.first_valid_index()]

        self.refactorThread = RefactorThread(self.refactorTimeframeBox.currentText(),
                                             self.dataWindow.symbolBox.currentText(), startDate, endDate)
        self.refactorThread.finished.connect(self.refactorFinished)
        self.refactorThread.start()

    def refactorFinished(self):
        self.refactorButton.setEnabled(True)
        del self.refactorThread

    def initRefactorBox(self):
        self.refactorTimeframeBox.setToolTip("RefactorTimeframe")
        self.refactorTimeframeBox.addItems(self.dataWindow.timeframeList)


class RefactorThread(QThread):
    def __init__(self, timeframe, symbol, startDate, endDate):
        super().__init__()
        self.timeframe = timeframe
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate

    def run(self):
        HistoricDataLoader.reformat_data(self.timeframe, self.symbol, False, self.startDate, self.endDate)
