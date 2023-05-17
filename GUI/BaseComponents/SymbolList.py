from GUI.BaseComponents.MultiSelectList import MultiSelectList


class SymbolList(MultiSelectList):
    def __init__(self, data=None):
        self.data = data

        if self.data is None:
            self.data = ["ES", "EURUSD"]

        super().__init__(self.data, "Symbol")
