
from datetime import timedelta
from .models import Holiday

def is_weekend(date):
    day = date.weekday()
    return day == 5 or day == 6  # Saturday or Sunday

def is_holiday(date):
    return Holiday.objects.filter(date=date).exists()

def calculate_business_days(start_date, end_date):
    current_date = start_date
    business_days = 0

    while current_date <= end_date:
        if not is_weekend(current_date) and not is_holiday(current_date):
            business_days += 1
        current_date += timedelta(days=1)

    return business_days
