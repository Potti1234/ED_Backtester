from Indicator.Indicator import Indicator


class Imbalance(Indicator):
    """
    Calculates Imbalances
    """

    def __init__(self, timeframe, symbol, period):
        """
        Initialises the Imbalance indicator.

        Parameters:
        timeframe - The timeframe to calculate the Indicator
        symbol - The symbol to calculate the Indicator
        period - The period to calculated the value
        """
        self.symbol = symbol
        self.period = period
        self.timeframe = timeframe
        self.indicator_values = []  # Format [Start, End]
        self.timestamp_values = []

    def calculate_indicator(self, data, is_new_candle, is_last_candle):
        if len(data[4]) < 1:
            return

        close = data[4][-self.period:]

        # SMA if available data is lower than period or the first data
        if len(self.indicator_values) < self.period:
            self.SMA.calculate_indicator(data, is_new_candle, is_last_candle)
            indicator_value = self.SMA.return_value(0)

            if is_new_candle is True:
                self.indicator_values.append(indicator_value)
                self.timestamp_values.append(data[0][-1])
            elif is_new_candle is False:
                try:
                    self.indicator_values[-1] = indicator_value
                    self.timestamp_values[-1] = data[0][-1]
                except IndexError:
                    self.indicator_values.append(indicator_value)
                    self.timestamp_values.append(data[0][-1])
        # EMA calculation if there are enough values
        else:
            if is_new_candle is True:
                indicator_value = (close[-1] * self.multiplier) + (self.indicator_values[-1] * (1 - self.multiplier))
                self.indicator_values.append(indicator_value)
                self.timestamp_values.append(data[0][-1])
            elif is_new_candle is False:
                try:
                    indicator_value = (close[-1] * self.multiplier) + (self.indicator_values[-2] * (1 - self.multiplier))
                    self.indicator_values[len(self.indicator_values) - 1] = indicator_value
                    self.timestamp_values[-1] = data[0][-1]
                except IndexError:
                    indicator_value = (close[-1] * self.multiplier) + (
                                self.indicator_values[-1] * (1 - self.multiplier))
                    self.indicator_values.append(indicator_value)
                    self.timestamp_values.append(data[0][-1])

    def return_value(self, shift, timestamp=False):
        """

        Args:
            shift: The amount of bars to go back
            timestamp: return timestamp

        Returns:
            The value of the indicator

        """
        if timestamp is False:
            try:
                return self.indicator_values[-shift - 1]
            except IndexError:
                return []
        elif timestamp is True:
            try:
                return self.timestamp_values[-shift - 1]
            except IndexError:
                return []

    def return_all_values(self, timestamp=False):
        if timestamp is False:
            return self.indicator_values
        elif timestamp is True:
            return self.timestamp_values


"""
// This source code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/

// Update
//   - update screenshot
//   - add alerts
//   - fix deletion of triggered zone
//   - update screenshot
//   - add mid lines to imbalanced boxes
//   - add color option for each box type

//@version=5
indicator(title='Imbalanced zone', overlay=true)

penetrationRatio = input.float(defval=0.2, minval=0, maxval=1, step=0.1, title="Penetration Ratio")
extendBoxes = input.bool(defval=true, title="Extend boxes")
imbalancedDownColor = input.color(color.rgb(120,120,120,60), title="Box color", group="Imbalanced down")
imbalancedDownMidLineColor = input.color(color.rgb(120,120,120), title="Mid line color", group="Imbalanced down")
imbalancedUpColor = input.color(color.rgb(120,120,120,60), title="Box color", group="Imbalanced up")
imbalancedUpMidLineColor = input.color(color.rgb(120,120,120), title="Mid line color", group="Imbalanced up")

var box[] imbalancedDownBoxes = array.new_box()
var box[] imbalancedUpBoxes = array.new_box()
var line[] imbalancedDownMidLines = array.new_line()
var line[] imbalancedUpMidLines = array.new_line()

extension = extend.none
if extendBoxes
    extension := extend.right

if high[3] < low[1]
    array.push(imbalancedDownBoxes, box.new(left=bar_index - 2, bottom=high[3], right=bar_index + 20, top=low[1], bgcolor=imbalancedDownColor, border_color=imbalancedDownColor, extend=extension))
    midPoint = (high[3]-low[1])/2+low[1]
    array.push(imbalancedDownMidLines, line.new(bar_index - 2, midPoint, bar_index+20, midPoint, style=line.style_dotted, extend=extension, color=imbalancedDownMidLineColor))
if low[3] > high[1]
    array.push(imbalancedUpBoxes, box.new(left=bar_index - 2, top=low[3], right=bar_index + 20, bottom=high[1], bgcolor=imbalancedUpColor, border_color=imbalancedUpColor, extend=extension))
    midPoint = (high[1]-low[3])/2+low[3]
    array.push(imbalancedUpMidLines, line.new(bar_index - 2, midPoint, bar_index+20, midPoint, style=line.style_dotted, extend=extension, color=imbalancedUpMidLineColor))

if array.size(imbalancedUpBoxes) > 0
    for i = array.size(imbalancedUpBoxes) - 1 to 0 by 1
        imbalancedBox = array.get(imbalancedUpBoxes, i)
        top = box.get_top(imbalancedBox)
        bottom = box.get_bottom(imbalancedBox)
        invalidationLimit = (top - bottom) * penetrationRatio
        box.set_right(imbalancedBox, bar_index + 20)

        midLine = array.get(imbalancedUpMidLines, i)
        line.set_x2(midLine, bar_index + 20)

        if high >= bottom + invalidationLimit
            box.delete(imbalancedBox)
            array.remove(imbalancedUpBoxes, i)
            line.delete(midLine)
            array.remove(imbalancedUpMidLines, i)

if array.size(imbalancedDownBoxes) > 0
    for i = array.size(imbalancedDownBoxes) - 1 to 0 by 1
        imbalancedBox = array.get(imbalancedDownBoxes, i)
        top = box.get_top(imbalancedBox)
        bottom = box.get_bottom(imbalancedBox)
        invalidationLimit = (top - bottom) * penetrationRatio
        box.set_right(imbalancedBox, bar_index + 20)

        midLine = array.get(imbalancedDownMidLines, i)
        line.set_x2(midLine, bar_index + 20)

        if low <= top - invalidationLimit
            box.delete(imbalancedBox)
            array.remove(imbalancedDownBoxes, i)
            line.delete(midLine)
            array.remove(imbalancedDownMidLines, i)

// Alerts
alertcondition(high[3] < low[1] or low[3] > high[1], title="New imbalanced candle")
"""
