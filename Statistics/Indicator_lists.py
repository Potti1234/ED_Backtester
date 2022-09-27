def return_MSLPinbarIndicators():
    indicator_list = [["MajorSwingLevel1H", "Line_chart", "Main_Plot", "MajorSwingLevels", "1hour", "red"],
                      ["MajorSwingLevel4H", "Line_chart", "Main_Plot", "MajorSwingLevels", "4hour", "blue"],
                      ["ATR", "Line_chart", "Sub_Plot", "ATR", "1hour", "blue"],
                      ["Pinbar", "Line_chart", "Sub_Plot", "Pinbar", "1hour", "blue"],
                      ["EngulfingCandle", "Line_chart", "Sub_Plot", "EngulfingCandle", "1hour", "blue"],
                      ["TrendFilter1H", "Line_chart", "Sub_Plot", "TrendFilter1H", "1hour", "blue"],
                      ["TrendFilter4H", "Line_chart", "Sub_Plot", "TrendFilter4H", "4hour", "blue"]]
    return indicator_list


def return_MSLReversalIndicators():
    indicator_list = [["MajorSwingLevels4H", "Line_chart", "Main_Plot", "MajorSwingLevels", "4hour", "blue"],
                      ["TrendFilter4H", "Line_chart", "Sub_Plot", "TrendFilter4H", "4hour", "blue"],
                      ["ATR15M", "Line_chart", "Sub_Plot", "ATR", "15minute", "blue"]]
    return indicator_list


def return_MSLBreakoutIndicators():
    indicator_list = [["MajorSwingLevels15m", "Line_chart", "Main_Plot", "MajorSwingLevels", "15minute", "blue"],
                      ["MajorSwingLevels4H", "Line_chart", "Main_Plot", "MajorSwingLevels", "4hour", "blue"],
                      ["TrendFilter15m", "Line_chart", "Sub_Plot", "TrendFilter4H", "15minute", "blue"],
                      ["TrendFilter4H", "Line_chart", "Sub_Plot", "TrendFilter4H", "4hour", "blue"],
                      ["ATR15M", "Line_chart", "Sub_Plot", "ATR", "15minute", "blue"]]
    return indicator_list
