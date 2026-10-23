import os
import pandas as pd

from data_handler import load_electricity_data

from consumption import (
    calculate_daily_consumption,
    calculate_monthly_consumption,
    calculate_average_consumption,
    find_highest_consumption_day,
    find_lowest_consumption_day
)

from bill_calculator import calculate_electricity_bill

from anomaly_detector import (
    detect_unusual_consumption,
    get_unusual_consumption_days
)

from visualizer import (
    plot_daily_consumption,
    plot_monthly_consumption
)


DATA_FILE = os.path.join(
    "data",
    "electricity_data.csv"
)

REPORT_FOLDER = "reports"


def display_daily_consumption(df):
    """
    Display daily electricity consumption.
    """

    print("\n--- DAILY ELECTRICITY CONSUMPTION ---")

    columns = [
        "date",
        "meter_reading",
        "daily_consumption"
    ]

    print(
        df[columns].to_string(
            index=False
        )
    )


def display_monthly_summary(df):
    """
    Display the monthly consumption summary.
    """

    print("\n--- MONTHLY CONSUMPTION SUMMARY ---")

    monthly_summary = calculate_monthly_consumption(df)

    if monthly_summary.empty:
        print("No monthly consumption data available.")
        return

    print(monthly_summary.round(2).to_string())


def display_usage_statistics(df):
    """
    Display average, highest, and lowest usage.
    """

    print("\n--- ELECTRICITY USAGE STATISTICS ---")

    average = calculate_average_consumption(df)

    print(f"Average daily consumption: {average:.2f} kWh")

    highest = find_highest_consumption_day(df)
    lowest = find_lowest_consumption_day(df)

    if highest is not None:
        print(
            f"Highest usage: {highest['daily_consumption']:.2f} kWh "
            f"on {highest['date'].strftime('%Y-%m-%d')}"
        )

    if lowest is not None:
        print(
            f"Lowest usage: {lowest['daily_consumption']:.2f} kWh "
            f"on {lowest['date'].strftime('%Y-%m-%d')}"
        )


def estimate_monthly_bill(df):
    """
    Estimate the bill for a month selected by the user.
    """

    monthly_summary = calculate_monthly_consumption(df)

    if monthly_summary.empty:
        print("No monthly consumption data available.")
        return

    print("\nAvailable months:")

    for month in monthly_summary.index:
        print(month)

    selected_month = input(
        "\nEnter month in YYYY-MM format: "
    ).strip()

    try:
        month = pd.Period(
            selected_month,
            freq="M"
        )
    except ValueError:
        print("Invalid month format. Example: 2026-10")
        return

    if month not in monthly_summary.index:
        print("The selected month is not available.")
        return

    units = float(
        monthly_summary.loc[
            month,
            "total_consumption"
        ]
    )

    bill = calculate_electricity_bill(units)

    print(f"\nSelected month: {month}")
    print(f"Recorded consumption: {units:.2f} kWh")
    print(f"Estimated energy charges: Rs. {bill:.2f}")
    print(
        "Note: This is an estimate using sample tariff slabs, "
        "not an official electricity bill."
    )


def display_unusual_usage(df):
    """
    Detect and display unusual consumption.
    """

    print("\n--- UNUSUAL USAGE DETECTION ---")

    result = detect_unusual_consumption(df)

    unusual_days = get_unusual_consumption_days(result)

    if unusual_days.empty:
        print(
            "No unusual consumption was detected "
            "using the current rule."
        )
        print(
            "Note: This does not guarantee that all usage is normal."
        )
        return

    columns = [
        "date",
        "daily_consumption",
        "previous_7_day_average"
    ]

    print(
        unusual_days[columns].to_string(
            index=False
        )
    )

    print(
        "\nThese readings are flagged for review, "
        "not confirmed faults."
    )


def export_reports(df):
    """
    Export daily and monthly reports to CSV files.
    """

    os.makedirs(
        REPORT_FOLDER,
        exist_ok=True
    )

    daily_file = os.path.join(
        REPORT_FOLDER,
        "daily_report.csv"
    )

    monthly_file = os.path.join(
        REPORT_FOLDER,
        "monthly_report.csv"
    )

    df.to_csv(
        daily_file,
        index=False
    )

    monthly_summary = calculate_monthly_consumption(df)

    monthly_summary.to_csv(
        monthly_file
    )

    print("\nReports generated successfully!")
    print(f"Daily report: {daily_file}")
    print(f"Monthly report: {monthly_file}")


def display_menu():
    """
    Display the main menu.
    """

    print("\n======================================")
    print(" HOUSEHOLD ELECTRICITY USAGE ANALYZER ")
    print("======================================")

    print("1. View Daily Consumption")
    print("2. View Monthly Summary")
    print("3. View Usage Statistics")
    print("4. Estimate Electricity Bill")
    print("5. Detect Unusual Usage")
    print("6. Generate Daily Graph")
    print("7. Generate Monthly Graph")
    print("8. Export Reports")
    print("9. Exit")


def main():
    """
    Main function of the application.
    """

    print("Loading electricity meter readings...")

    df = load_electricity_data(DATA_FILE)

    if df is None:
        print(
            "Application stopped because the data "
            "could not be loaded."
        )
        return

    df = calculate_daily_consumption(df)

    print("Data loaded and validated successfully!")

    while True:

        display_menu()

        choice = input(
            "\nEnter your choice (1-9): "
        ).strip()

        try:

            if choice == "1":
                display_daily_consumption(df)

            elif choice == "2":
                display_monthly_summary(df)

            elif choice == "3":
                display_usage_statistics(df)

            elif choice == "4":
                estimate_monthly_bill(df)

            elif choice == "5":
                display_unusual_usage(df)

            elif choice == "6":
                plot_daily_consumption(df)

            elif choice == "7":
                monthly_summary = calculate_monthly_consumption(df)

                plot_monthly_consumption(
                    monthly_summary
                )

            elif choice == "8":
                export_reports(df)

            elif choice == "9":
                print(
                    "\nThank you for using the "
                    "Household Electricity Usage Analyzer!"
                )
                break

            else:
                print(
                    "Invalid choice. Please enter a number "
                    "between 1 and 9."
                )

        except (ValueError, OSError) as error:
            print(f"Unable to complete the operation: {error}")

        except Exception as error:
            print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    main()