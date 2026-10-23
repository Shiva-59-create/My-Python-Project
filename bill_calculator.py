def calculate_electricity_bill(units):
    """
    Estimate the electricity bill using sample progressive tariff slabs.

    First 50 units: Rs. 1.50 per unit
    Next 50 units: Rs. 2.50 per unit
    Above 100 units: Rs. 4.00 per unit

    These are illustrative rates, not official electricity tariffs.
    """

    if units < 0:
        raise ValueError("Units cannot be negative.")

    if units <= 50:
        bill = units * 1.50

    elif units <= 100:
        bill = (
            50 * 1.50
            + (units - 50) * 2.50
        )

    else:
        bill = (
            50 * 1.50
            + 50 * 2.50
            + (units - 100) * 4.00
        )

    return round(bill, 2)