from PyQt5.QtWidgets import *
from DataWindow.DataWindow import DataWindow
from GUI.StatisticsWindow.StatisticsWindow import StatisticsWindow
from GUI.BacktestWindow.BacktestWindow import BacktestWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dataWindow = DataWindow()
        self.statisticsWindow = StatisticsWindow()
        self.backtestWindow = BacktestWindow()

        self.setWindowTitle("Backtester")
        self.initLayout()
        self.initMenu()

    def initLayout(self):
        dataButton = QPushButton("Data")
        statisticsButton = QPushButton("Statistics")
        backtestButton = QPushButton("Backtest")

        dataButton.clicked.connect(self.dataButtonClicked)
        statisticsButton.clicked.connect(self.statisticsButtonClicked)
        backtestButton.clicked.connect(self.backtestButtonClicked)

        layout = QVBoxLayout()
        layout.addWidget(dataButton)
        layout.addWidget(statisticsButton)
        layout.addWidget(backtestButton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def initMenu(self):
        menu = self.menuBar()

        dataAction = QAction("Data Window", self)
        dataAction.setStatusTip("Opens the Data Window")
        dataAction.triggered.connect(self.dataButtonClicked)

        statisticsAction = QAction("Statistics Window", self)
        statisticsAction.setStatusTip("Opens the Statistics Window")
        statisticsAction.triggered.connect(self.dataButtonClicked)

        backtestAction = QAction("Backtest Window", self)
        backtestAction.setStatusTip("Opens the Backtest Window")
        backtestAction.triggered.connect(self.dataButtonClicked)

        dataMenu = menu.addMenu("Data")
        dataMenu.addAction(dataAction)
        dataMenu.addSeparator()

        statisticsMenu = menu.addMenu("Statistics")
        statisticsMenu.addAction(statisticsAction)
        statisticsMenu.addSeparator()

        backtestMenu = menu.addMenu("Backtest")
        backtestMenu.addAction(backtestAction)
        backtestMenu.addSeparator()

    def dataButtonClicked(self):
        self.dataWindow.show()

    def statisticsButtonClicked(self):
        self.statisticsWindow.show()

    def backtestButtonClicked(self):
        self.backtestWindow.show()


if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()
