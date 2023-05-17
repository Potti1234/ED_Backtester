from GUI.BaseComponents.MultiSelectList import MultiSelectList


class TimeframeList(MultiSelectList):
    def __init__(self, data=None):
        self.data = data

        if self.data is None:
            self.data = ["1minute", "5minute", "15minute", "30minute", "1hour", "4hour", "1day"]

        super().__init__(self.data, "Timeframe")
