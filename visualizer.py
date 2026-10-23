import os
import matplotlib.pyplot as plt


def plot_daily_consumption(df):
    """
    Generate a line graph of daily electricity consumption.
    """

    os.makedirs("reports", exist_ok=True)

    valid_data = df.dropna(
        subset=["daily_consumption"]
    )

    if valid_data.empty:
        print("Not enough data to generate a daily graph.")
        return

    plt.figure(figsize=(10, 5))

    plt.plot(
        valid_data["date"],
        valid_data["daily_consumption"],
        marker="o"
    )

    plt.title("Daily Household Electricity Consumption")
    plt.xlabel("Date")
    plt.ylabel("Consumption (kWh)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(
        "reports/daily_consumption.png"
    )

    print(
        "Daily consumption graph saved to "
        "reports/daily_consumption.png"
    )

    plt.show()
    plt.close()


def plot_monthly_consumption(monthly_summary):
    """
    Generate a bar chart of monthly electricity consumption.
    """

    os.makedirs("reports", exist_ok=True)

    if monthly_summary.empty:
        print("No monthly data available.")
        return

    plt.figure(figsize=(9, 5))

    months = monthly_summary.index.astype(str)

    plt.bar(
        months,
        monthly_summary["total_consumption"]
    )

    plt.title("Monthly Household Electricity Consumption")
    plt.xlabel("Month")
    plt.ylabel("Total Consumption (kWh)")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()

    plt.savefig(
        "reports/monthly_consumption.png"
    )

    print(
        "Monthly consumption graph saved to "
        "reports/monthly_consumption.png"
    )

    plt.show()
    plt.close()