from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout, QCheckBox, QScrollArea, \
    QPushButton
from PyQt5.QtCore import Qt


class MultiSelectList(QWidget):
    def __init__(self, data, title="Data"):
        super().__init__()
        self.data = data

        # Create a table widget to display the data
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setRowCount(len(self.data))
        self.table.setHorizontalHeaderLabels([title, "Select"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populate the table with the first 5 timeframes and checkboxes
        for i in range(len(self.data)):
            item_timeframe = QTableWidgetItem(self.data[i])
            self.table.setItem(i, 0, item_timeframe)

            checkbox = QCheckBox()
            checkbox.setChecked(True)
            self.table.setCellWidget(i, 1, checkbox)

        # Create a scroll area and add the table to it
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.table)

        # Add a button to deselect all checkboxes
        deselect_button = QPushButton('Deselect All')
        deselect_button.clicked.connect(self.deselect_all)

        # Add the scroll area to the layout
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        layout.addWidget(deselect_button)

        self.setLayout(layout)

    def get_selected_rows(self):
        # Iterate over the rows in the table and get the selected timeframes
        selected_timeframes = []
        for i in range(self.table.rowCount()):
            checkbox = self.table.cellWidget(i, 1)
            if checkbox.isChecked():
                item_timeframe = self.table.item(i, 0)
                selected_timeframes.append(item_timeframe.text())

        # Print the selected timeframes
        return selected_timeframes

    def deselect_all(self):
        for i in range(self.table.rowCount()):
            item = self.table.cellWidget(i, 1)
            item.setCheckState(Qt.Unchecked)

    def select(self, newList):
        self.deselect_all()
        for i in range(self.table.rowCount()):
            item = self.table.item(i, 0)
            text = item.text()
            if text in newList:
                self.table.cellWidget(i, 1).setCheckState(Qt.Checked)
