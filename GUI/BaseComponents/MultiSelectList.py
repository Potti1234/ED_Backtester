from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QCheckBox, QScrollArea, \
    QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt


class MultiSelectList(QWidget):
    def __init__(self, data, title="Data"):
        super().__init__()
        self.data = data

        # Create a table widget to display the data
        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.columnCount = 1
        self.table.setRowCount(len(self.data))
        self.table.setHorizontalHeaderLabels([title])
        self.headers = [title]
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with the items
        for i in range(len(self.data)):
            item = QTableWidgetItem(self.data[i])
            self.table.setItem(i, 0, item)

        self.addCheckboxColumn()

        self.layout = QVBoxLayout()

        self.selectLayout = QHBoxLayout()
        self.addDeselectAllButton()
        self.addSelectAllButton()
        self.layout.addLayout(self.selectLayout)

        self.addScrollArea()

        self.setLayout(self.layout)

    def addDeselectAllButton(self):
        deselectButton = QPushButton('Deselect All')
        deselectButton.clicked.connect(self.deselectAll)
        self.selectLayout.addWidget(deselectButton)

    def addSelectAllButton(self):
        selectButton = QPushButton('Select All')
        selectButton.clicked.connect(self.selectAll)
        self.selectLayout.addWidget(selectButton)

    def addScrollArea(self):
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table)
        self.layout.addWidget(scroll_area)

    def addCheckboxColumn(self, columnNumber=1, columnName="Select"):
        self.columnCount += 1
        self.table.setColumnCount(self.columnCount)
        self.headers.append(columnName)
        self.table.setHorizontalHeaderLabels(self.headers)
        for i in range(len(self.data)):
            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.table.setCellWidget(i, columnNumber, checkbox)

    def addTextFieldColumn(self, columnNumber=2, columnName="Text", values=None):
        self.columnCount += 1
        self.table.setColumnCount(self.columnCount)
        self.headers.append(columnName)
        self.table.setHorizontalHeaderLabels(self.headers)
        for i in range(len(self.data)):
            textField = QLineEdit()
            if values is not None:
                textField.setText(str(values[i]))
            self.table.setCellWidget(i, columnNumber, textField)

    def getSelectedRows(self, columnNumberCheckBox=1, columnNumberTextField=0):
        selectedItems = []
        for i in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(i, columnNumberCheckBox)
            if checkbox.isChecked():
                item = self.table.cellWidget(i, columnNumberTextField)
                if columnNumberTextField == 0:
                    item = self.table.item(i, columnNumberTextField)
                selectedItems.append(item.text())

        return selectedItems

    def deselectAll(self):
        for i in range(self.table.rowCount()):
            item = self.table.cellWidget(i, 1)
            item.setCheckState(Qt.Unchecked)

    def selectAll(self):
        for i in range(self.table.rowCount()):
            item = self.table.cellWidget(i, 1)
            item.setCheckState(Qt.Checked)

    def select(self, newList):
        self.deselectAll()
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            text = item.text()
            if text in newList:
                self.table.cellWidget(i, 1).setCheckState(Qt.Checked)
