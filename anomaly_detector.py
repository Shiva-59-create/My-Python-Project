def detect_unusual_consumption(df, threshold=1.5):
    """
    Detect unusually high electricity consumption.

    A day is flagged if its consumption is greater than
    threshold multiplied by the average consumption
    of the previous seven days.

    The current day is excluded from the average.
    """

    result = df.copy()

    result["previous_7_day_average"] = (
        result["daily_consumption"]
        .shift(1)
        .rolling(window=7, min_periods=7)
        .mean()
    )

    result["unusual_usage"] = (
        result["daily_consumption"]
        >
        threshold * result["previous_7_day_average"]
    )

    # Do not flag rows without enough historical data
    result["unusual_usage"] = (
        result["unusual_usage"]
        .fillna(False)
        .astype(bool)
    )

    return result


def get_unusual_consumption_days(df):
    """
    Return only days flagged for unusual consumption.
    """

    return df[df["unusual_usage"]].copy()