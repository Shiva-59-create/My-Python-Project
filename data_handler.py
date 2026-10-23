import pandas as pd


def load_electricity_data(file_path):
    """
    Load electricity meter readings from a CSV file.
    Validate the dates and meter readings.
    """

    try:
        df = pd.read_csv(file_path)

        # Check required columns
        required_columns = {"date", "meter_reading"}

        if not required_columns.issubset(df.columns):
            raise ValueError(
                "CSV must contain 'date' and 'meter_reading' columns."
            )

        # Reject missing values
        if df["date"].isna().any():
            raise ValueError("Some dates are missing.")

        if df["meter_reading"].isna().any():
            raise ValueError("Some meter readings are missing.")

        # Convert dates
        df["date"] = pd.to_datetime(
            df["date"],
            errors="raise"
        )

        # Convert readings to numbers
        df["meter_reading"] = pd.to_numeric(
            df["meter_reading"],
            errors="raise"
        )

        # Reject infinite or invalid numerical readings
        if not df["meter_reading"].map(
            lambda value: pd.notna(value) and abs(value) != float("inf")
        ).all():
            raise ValueError("Meter readings must be finite numbers.")

        # Reject negative readings
        if (df["meter_reading"] < 0).any():
            raise ValueError("Meter readings cannot be negative.")

        # Reject duplicate dates
        if df["date"].duplicated().any():
            raise ValueError("Duplicate dates found in the dataset.")

        # Sort by date
        df = df.sort_values("date").reset_index(drop=True)

        # Require consecutive calendar days for daily analysis
        if len(df) > 1:
            date_gaps = df["date"].diff().dropna()

            if not (date_gaps == pd.Timedelta(days=1)).all():
                raise ValueError(
                    "Dates must be consecutive calendar days. "
                    "Please add any missing daily readings."
                )

        # Reject decreasing meter readings
        if (df["meter_reading"].diff().dropna() < 0).any():
            raise ValueError(
                "A meter reading is lower than the previous reading. "
                "Check for data errors or a meter reset."
            )

        if len(df) < 2:
            raise ValueError(
                "At least two consecutive daily readings are required."
            )

        return df

    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None

    except pd.errors.EmptyDataError:
        print("Error: The CSV file is empty.")
        return None

    except (ValueError, TypeError) as error:
        print(f"Data validation error: {error}")
        return None

    except Exception as error:
        print(f"Unexpected error while loading data: {error}")
        return None