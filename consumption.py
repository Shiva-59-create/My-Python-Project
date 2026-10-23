import pandas as pd
import numpy as np


def calculate_daily_consumption(df):
    """
    Calculate daily electricity consumption.

    Daily consumption =
    Current meter reading - Previous meter reading
    """

    result = df.copy()

    result["daily_consumption"] = (
        result["meter_reading"].diff()
    )

    return result


def calculate_monthly_consumption(df):
    """
    Calculate monthly electricity consumption.
    """

    result = df.dropna(
        subset=["daily_consumption"]
    ).copy()

    result["month"] = (
        result["date"].dt.to_period("M")
    )

    monthly_summary = result.groupby("month").agg(
        total_consumption=("daily_consumption", "sum"),
        average_daily_consumption=("daily_consumption", "mean"),
        highest_daily_consumption=("daily_consumption", "max"),
        lowest_daily_consumption=("daily_consumption", "min")
    )

    return monthly_summary


def calculate_average_consumption(df):
    """
    Calculate average daily consumption.
    """

    usage = df["daily_consumption"].dropna()

    if usage.empty:
        return 0

    return float(np.mean(usage))


def find_highest_consumption_day(df):
    """
    Find the day with the highest electricity consumption.
    """

    usage = df.dropna(
        subset=["daily_consumption"]
    )

    if usage.empty:
        return None

    return usage.loc[
        usage["daily_consumption"].idxmax()
    ]


def find_lowest_consumption_day(df):
    """
    Find the day with the lowest electricity consumption.
    """

    usage = df.dropna(
        subset=["daily_consumption"]
    )

    if usage.empty:
        return None

    return usage.loc[
        usage["daily_consumption"].idxmin()
    ]