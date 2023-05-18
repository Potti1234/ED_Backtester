from GUI.BaseComponents.MultiSelectList import MultiSelectList
import pandas as pd


class VariableList(MultiSelectList):
    """
    A list of all variables of a trades.csv file with a checkbox and a input field to enter a round parameter
    """
    def __init__(self, filename):
        self.filename = filename

        df = pd.read_csv(filename)
        df = df.select_dtypes(exclude=['object'])
        self.data = list(df.columns)

        super().__init__(self.data, "Variables")

        defaultRoundValues = list(df.apply(lambda x: round(((x.max() - x.min()) / 100), 2)))

        self.addTextFieldColumn(2, "RoundValue", defaultRoundValues)
