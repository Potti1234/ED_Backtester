from PyQt5.QtWidgets import *
from GUI.BaseComponents.SymbolList import SymbolList
from GUI.BaseComponents.TimeframeList import TimeframeList
from GUI.BacktestWindow.BacktestWindow import getAllSubClassesOfAbstractClass
from Statistics.Statistics import Statistics
import os
import inspect
import importlib
from collections import OrderedDict
from Statistics.Main_Statistics import load_data
from GUI.StatisticsWindow.VariableList import VariableList


class StatisticsWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.strategyLayout = QHBoxLayout()
        self.strategyComboBox = QComboBox()

        self.universeLayout = QHBoxLayout()
        self.symbolList = SymbolList()
        self.timeframeList = TimeframeList()

        self.dateLayout = QHBoxLayout()
        self.startDateField = QDateEdit()
        self.endDateField = QDateEdit()

        self.statisticsLayout = QHBoxLayout()
        self.statisticsComboBox = QComboBox()
        self.statisticsParameters = []

        self.controleLayout = QHBoxLayout()
        self.saveNameField = QLineEdit()
        self.saveButton = QPushButton()

        self.initLayout()

    def initLayout(self):
        self.initStrategyLayout()
        self.initUniverseLayout()
        self.initDateLayout()
        self.initStatisticsLayout()
        self.initControleLayout()

        self.layout.addLayout(self.strategyLayout)
        self.layout.addLayout(self.universeLayout)
        self.layout.addLayout(self.dateLayout)
        self.layout.addLayout(self.statisticsLayout)
        self.layout.addLayout(self.controleLayout)

        self.setLayout(self.layout)

    def initStrategyLayout(self):
        self.strategyComboBox.setToolTip("Strategy")
        folders = [f for f in os.listdir("D:\\AktienDaten\\Statistics") if os.path.isdir("D:\\AktienDaten\\Statistics\\" + f)]
        self.strategyComboBox.addItems(folders)
        self.strategyComboBox.currentTextChanged.connect(self.strategyChanged)

        self.strategyLayout.addWidget(self.strategyComboBox)

    def initDateLayout(self):
        self.startDateField.setDisplayFormat("yyyy-MM-dd")
        self.endDateField.setDisplayFormat("yyyy-MM-dd")

        self.startDateField.setToolTip("StartDate")
        self.endDateField.setToolTip("EndDate")

        self.dateLayout.addWidget(self.startDateField)
        self.dateLayout.addWidget(self.endDateField)

    def initUniverseLayout(self):
        self.universeLayout.addWidget(self.symbolList)
        self.universeLayout.addWidget(self.timeframeList)

    def initStatisticsLayout(self):
        self.statisticsComboBox.setToolTip("Statistics")
        self.statisticsComboBox.addItems(getAllSubClassesOfAbstractClass("Statistics", Statistics))
        self.statisticsComboBox.currentTextChanged.connect(self.statisticChanged)

        self.statisticsLayout.addWidget(self.statisticsComboBox)

    def statisticChanged(self):
        module = importlib.import_module("Statistics." + self.statisticsComboBox.currentText())
        parameters = OrderedDict
        for name, obj in inspect.getmembers(module):
            if name == self.statisticsComboBox.currentText():
                parameters = inspect.signature(obj).parameters

        for widget in self.statisticsParameters:
            self.statisticsLayout.removeWidget(widget)
        self.statisticsParameters = []

        for param, value in parameters.items():
            if param == "df":
                continue
            elif param == "variable_list":
                widget = VariableList("D:\\AktienDaten\\Statistics\\" + self.strategyComboBox.currentText() + "\\" +
                                      self.symbolList.data[0] + "\\Trades.csv")
            else:
                widget = QLineEdit()
                widget.setToolTip(param)
                if value.default is not inspect.Parameter.empty and value.default is not None:
                    widget.setText(str(value.default))
            self.statisticsParameters.append(widget)
            self.statisticsLayout.addWidget(widget)

    def initControleLayout(self):
        self.saveNameField.setToolTip("SaveName")
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)

        self.controleLayout.addWidget(self.saveNameField)
        self.controleLayout.addWidget(self.saveButton)

    def save(self):
        # Add start, end date to load data
        # Get indicator list
        for symbol in self.symbolList.getSelectedRows():
            for timeframe in self.timeframeList.getSelectedRows():
                params = (load_data(self.strategyComboBox.currentText(), symbol, timeframe, []),)
                for widget in self.statisticsParameters:
                    if isinstance(widget, QLineEdit):
                        params = params + (widget.text(),)
                    elif isinstance(widget, VariableList):
                        variableList = [[a, b] for a, b in zip(widget.getSelectedRows(1, 0), widget.getSelectedRows(1, 2))]
                        params = params + (variableList,)
                    else:
                        print("Data of " + str(type(widget)) + " can not be read")

                mymodule = importlib.import_module("Statistics." + self.statisticsComboBox.currentText())
                classObject = getattr(mymodule, self.statisticsComboBox.currentText())

                instance = classObject(*params)

                instance.plot_results(self.saveNameField.text())

    def strategyChanged(self):
        self.universeLayout.removeWidget(self.symbolList)
        self.universeLayout.removeWidget(self.timeframeList)

        symbols = [f for f in os.listdir("D:\\AktienDaten\\Statistics\\" + self.strategyComboBox.currentText()) if
                   os.path.isdir("D:\\AktienDaten\\Statistics\\" + self.strategyComboBox.currentText() + "\\" + f)]
        self.symbolList = SymbolList(symbols)

        self.universeLayout.addWidget(self.symbolList)
        self.universeLayout.addWidget(self.timeframeList)
