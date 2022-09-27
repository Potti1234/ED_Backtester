def is_premarket(data, open_time, close_time):
    time = data % (60 * 60 * 24)

    if open_time < close_time:
        if time < open_time or time > close_time:
            return "PreMarket"
        elif open_time <= time <= close_time:
            return "Market"
    elif open_time > close_time:
        if open_time >= time >= close_time:
            return "PreMarket"
        elif time > open_time or time < close_time:
            return "Market"
