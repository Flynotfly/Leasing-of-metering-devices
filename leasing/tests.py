from django.test import TestCase
from datetime import date
from .utils import generate_payment_dates


class GeneratePaymentDatesTest(TestCase):
    def test_generate_payment_dates_regular_case(self):
        """Test payment dates for a regular case with consistent day of the month."""
        start_date = date(2024, 1, 15)  # Start on January 15th
        period = 3  # 3 months

        expected_dates = [
            date(2024, 1, 15),
            date(2024, 2, 15),
            date(2024, 3, 15),
        ]

        result = generate_payment_dates(start_date, period)
        self.assertEqual(result, expected_dates)

    def test_generate_payment_dates_end_of_month(self):
        """Test payment dates when the start date is at the end of a month."""
        start_date = date(2024, 1, 31)  # Start on January 31st
        period = 3  # 3 months

        expected_dates = [
            date(2024, 1, 31),
            date(2024, 2, 29),  # February 2024 is a leap year
            date(2024, 3, 31),
        ]

        result = generate_payment_dates(start_date, period)
        self.assertEqual(result, expected_dates)

    def test_generate_payment_dates_short_month(self):
        """Test payment dates for months with fewer days."""
        start_date = date(2024, 3, 30)  # Start on March 30th
        period = 3  # 3 months

        expected_dates = [
            date(2024, 3, 30),
            date(2024, 4, 30),
            date(2024, 5, 30),
        ]

        result = generate_payment_dates(start_date, period)
        self.assertEqual(result, expected_dates)

    def test_generate_payment_dates_february_non_leap_year(self):
        """Test payment dates spanning February in a non-leap year."""
        start_date = date(2023, 1, 31)  # Start on January 31st
        period = 3  # 3 months

        expected_dates = [
            date(2023, 1, 31),
            date(2023, 2, 28),  # February 2023 is not a leap year
            date(2023, 3, 31),
        ]

        result = generate_payment_dates(start_date, period)
        self.assertEqual(result, expected_dates)

    def test_generate_payment_dates_one_month(self):
        """Test a single payment month."""
        start_date = date(2024, 5, 10)  # Start on May 10th
        period = 1  # 1 month

        expected_dates = [date(2024, 5, 10)]

        result = generate_payment_dates(start_date, period)
        self.assertEqual(result, expected_dates)
