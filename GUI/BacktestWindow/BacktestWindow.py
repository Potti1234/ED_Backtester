import subprocess

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QDateEdit, QPushButton, QLineEdit
from GUI.BaseComponents.TimeframeList import TimeframeList
from GUI.BaseComponents.SymbolList import SymbolList
import inspect
import os
import importlib
from Universe.Universe import Universe
from Data.Data import DataHandler
from Portfolio.Portfolio import Portfolio
from RiskManagement.RiskManagement import RiskManagement
from Commission.Commission import Commission
from Execution.Execution import Execution
from Strategy.Strategy import Strategy


def getAllSubClassesOfAbstractClass(folderName, AbstractClass):
    file_names = [f for f in os.listdir("C:/Users/lukas/OneDrive/Dokumente/Pottibot/Backtester/ED_Backtester/" +
                                        folderName) if f.endswith(".py")]

    # Import each module and get its classes
    classes = []
    for file_name in file_names:
        module_name = file_name[:-3]  # Remove the .py extension
        module = importlib.import_module(folderName + "." + module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, AbstractClass) and obj is not AbstractClass:
                classes.append(obj.__name__)

    return classes


def listToString(inputList):
    resultList = "["
    for row in inputList:
        resultList += "\"" + row + "\", "
    resultList = resultList[:-2]
    resultList += "]"
    return resultList


class BacktestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.universeLayout = QHBoxLayout()
        self.universeComboBox = QComboBox()
        self.universeSymbolList = SymbolList()
        self.universeTimeframeList = TimeframeList()

        self.dataLayout = QHBoxLayout()
        self.dataComboBox = QComboBox()

        self.portfolioLayout = QHBoxLayout()
        self.portfolioComboBox = QComboBox()

        self.riskLayout = QHBoxLayout()
        self.riskComboBox = QComboBox()

        self.commissionLayout = QHBoxLayout()
        self.commissionComboBox = QComboBox()

        self.executionLayout = QHBoxLayout()
        self.executionComboBox = QComboBox()

        self.strategyLayout = QHBoxLayout()
        self.strategyComboBox = QComboBox()

        self.dateLayout = QHBoxLayout()
        self.startDateField = QDateEdit()
        self.endDateField = QDateEdit()

        self.backtestExecuteLayout = QHBoxLayout()
        self.nameField = QLineEdit()
        self.saveButton = QPushButton()
        self.backtesterComboBox = QComboBox()
        self.loadButton = QPushButton()
        self.startBacktestButton = QPushButton()

        self.initLayout()

    def initLayout(self):
        self.initUniverseLayout()
        self.initDataLayout()
        self.initPortfolioLayout()
        self.initRiskLayout()
        self.initCommissionLayout()
        self.initExecutionLayout()
        self.initStrategyLayout()
        self.initDateLayout()
        self.initBacktestExecuteLayout()

        self.layout.addLayout(self.dateLayout)
        self.layout.addLayout(self.backtestExecuteLayout)

        self.setLayout(self.layout)

    def initUniverseLayout(self):
        self.initBasicLayout(self.universeComboBox, self.universeLayout, "Universe", Universe)

        self.universeLayout.addWidget(self.universeSymbolList)
        self.universeLayout.addWidget(self.universeTimeframeList)

    def initDataLayout(self):
        self.initBasicLayout(self.dataComboBox, self.dataLayout, "Data", DataHandler)

    def initPortfolioLayout(self):
        self.initBasicLayout(self.portfolioComboBox, self.portfolioLayout, "Portfolio", Portfolio)

    def initRiskLayout(self):
        self.initBasicLayout(self.riskComboBox, self.riskLayout, "RiskManagement", RiskManagement)

    def initCommissionLayout(self):
        self.initBasicLayout(self.commissionComboBox, self.commissionLayout, "Commission", Commission)

    def initExecutionLayout(self):
        self.initBasicLayout(self.executionComboBox, self.executionLayout, "Execution", Execution)

    def initStrategyLayout(self):
        self.initBasicLayout(self.strategyComboBox, self.strategyLayout, "Strategy", Strategy)

    def initBasicLayout(self, comboBox, layout, name, AbstractClass):
        comboBox.setToolTip(name)
        comboBox.addItems(getAllSubClassesOfAbstractClass(name, AbstractClass))

        layout.addWidget(comboBox)
        self.layout.addLayout(layout)

    def initDateLayout(self):
        self.startDateField.setDisplayFormat("yyyy-MM-dd")
        self.endDateField.setDisplayFormat("yyyy-MM-dd")

        self.startDateField.setToolTip("StartDate")
        self.endDateField.setToolTip("EndDate")

        self.dateLayout.addWidget(self.startDateField)
        self.dateLayout.addWidget(self.endDateField)

    def initBacktestExecuteLayout(self):
        self.nameField.setToolTip("Name")
        self.saveButton.setText("Save")
        self.backtesterComboBox.setToolTip("Backtester To Load")
        file_names = [f for f in os.listdir("C:/Users/lukas/OneDrive/Dokumente/Pottibot/Backtester/ED_Backtester/Backtester") if f.endswith(".py")]
        self.backtesterComboBox.addItems(file_names)
        self.loadButton.setText("Load")
        self.startBacktestButton.setText("Start")

        self.saveButton.clicked.connect(self.save)
        self.loadButton.clicked.connect(self.load)
        self.startBacktestButton.clicked.connect(self.startBacktest)

        self.backtestExecuteLayout.addWidget(self.nameField)
        self.backtestExecuteLayout.addWidget(self.saveButton)
        self.backtestExecuteLayout.addWidget(self.backtesterComboBox)
        self.backtestExecuteLayout.addWidget(self.loadButton)
        self.backtestExecuteLayout.addWidget(self.startBacktestButton)

    def load(self):
        with open("C:/Users/lukas/OneDrive/Dokumente/Pottibot/Backtester/ED_Backtester/Backtester/" +
                  self.backtesterComboBox.currentText()[:-3] + ".txt", "r") as file:
            symbols = file.readline()[1:-2].replace("\"", "").split(", ")
            self.universeSymbolList.select(symbols)
            timeframes = file.readline()[1:-2].replace("\"", "").split(", ")
            self.universeTimeframeList.select(timeframes)
            self.universeComboBox.setCurrentText(file.readline()[:-1])
            self.dataComboBox.setCurrentText(file.readline()[:-1])
            self.strategyComboBox.setCurrentText(file.readline()[:-1])
            self.portfolioComboBox.setCurrentText(file.readline()[:-1])
            self.riskComboBox.setCurrentText(file.readline()[:-1])
            self.commissionComboBox.setCurrentText(file.readline()[:-1])
            self.executionComboBox.setCurrentText(file.readline()[:-1])
            self.nameField.setText(self.backtesterComboBox.currentText()[:-3])

    def save(self):
        universe = self.universeComboBox.currentText()
        data = self.dataComboBox.currentText()
        strategy = self.strategyComboBox.currentText()
        portfolio = self.portfolioComboBox.currentText()
        risk = self.riskComboBox.currentText()
        commission = self.commissionComboBox.currentText()
        execution = self.executionComboBox.currentText()

        code = "from Universe.{} import {} \n".format(universe, universe)
        code += "from Data.{} import {} \n".format(data, data)
        code += "from Strategy.{} import {} \n".format(strategy, strategy)
        code += "from Portfolio.{} import {} \n".format(portfolio, portfolio)
        code += "from RiskManagement.{} import {} \n".format(risk, risk)
        code += "from Commission.{} import {} \n".format(commission, commission)
        code += "from Execution.{} import {} \n".format(execution, execution)
        code += "from Backtester.Event_Driven_Backtester import Event_Driven_Backtester \n"
        code += "import queue \n"
        code += "import time \n"
        code += "from datetime import datetime \n\n\n"

        code += "def main():\n"
        code += "    statistics_filename = \"D:\\\\AktienDaten\\\\Statistics\\\\" + self.nameField.text() + "\\\\\" \n"
        code += "    csv_dir = \"D:\\\\AktienDaten\" \n"
        code += "    symbol_list = " + listToString(self.universeSymbolList.get_selected_rows()) + "\n"
        code += "    timeframe_list = " + listToString(self.universeTimeframeList.get_selected_rows()) + "\n"
        code += "    start_date = time.mktime(datetime.strptime(\"{}\", '%Y/%m/%d').timetuple()) \n".format(self.startDateField.text())
        code += "    end_date = time.mktime(datetime.strptime(\"{}\", '%Y/%m/%d').timetuple()) \n\n".format(self.endDateField.text())
        code += "    events = queue.Queue() \n\n"
        code += "    universe = {}(symbol_list) \n".format(universe)
        code += "    universe.initialise_symbol_list(\"EUR\") \n"
        code += "    bars = {}(events, csv_dir, universe, timeframe_list, start_date, end_date) \n".format(data)
        code += "    strategy = {}(events, bars) \n".format(strategy)
        code += "    risk = {}(bars, 1000) \n".format(risk)
        code += "    port = {}(bars, events, start_date, risk) \n".format(portfolio)
        code += "    commission = {}() \n".format(commission)
        code += "    broker = {}(events, commission) \n\n".format(execution)
        code += "    indicator_list = strategy.getIndicatorNames() \n\n"
        code += "    backtester = Event_Driven_Backtester(universe, bars, strategy, risk, port, commission, broker, events) \n"
        code += "    backtester.backtest() \n"
        code += "    backtester.save_statistics(statistics_filename, indicator_list) \n\n\n"
        code += "if __name__ == \"__main__\": \n"
        code += "    main() \n"

        with open("C:/Users/lukas/OneDrive/Dokumente/Pottibot/Backtester/ED_Backtester/Backtester/" + self.nameField.text() + ".py", "w") as file:
            file.write(code)

        saveData = listToString(self.universeSymbolList.get_selected_rows()) + "\n"
        saveData += listToString(self.universeTimeframeList.get_selected_rows()) + "\n"
        saveData += universe + "\n"
        saveData += data + "\n"
        saveData += strategy + "\n"
        saveData += portfolio + "\n"
        saveData += risk + "\n"
        saveData += commission + "\n"
        saveData += execution

        with open("C:/Users/lukas/OneDrive/Dokumente/Pottibot/Backtester/ED_Backtester/Backtester/" + self.nameField.text() + ".txt", "w") as file:
            file.write(saveData)

    def startBacktest(self):
        subprocess.call(["python", self.nameField.text() + ".py"])
