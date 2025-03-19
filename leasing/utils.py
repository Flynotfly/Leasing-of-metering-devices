from datetime import date, timedelta
from decimal import Decimal
import calendar

from .models import Payment


def generate_payment_dates(start_date: date, period: int) -> list[date]:
    payment_dates = []
    day = start_date.day
    current_date = start_date

    for _ in range(period):
        month = current_date.month
        year = current_date.year
        last_day_of_month = calendar.monthrange(year, month)[1]

        # Ensure the day does not exceed the last day of the month
        payment_day = min(day, last_day_of_month)
        payment_date = date(year, month, payment_day)
        payment_dates.append(payment_date)

        # Move to the next month
        if month == 12:
            current_date = date(year + 1, 1, 1)
        else:
            current_date = date(year, month + 1, 1)

    return payment_dates


def create_payments(contract, payment_dates: list[date], monthly_payment: Decimal):
    for payment_date in payment_dates:
        Payment.objects.create(
            contract=contract,
            amount=monthly_payment,
            date=payment_date
        )
