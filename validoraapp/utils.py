from datetime import time
from pytz import timezone as pytz_timezone
from .models import Appointment


from datetime import time, timedelta
from django.utils.timezone import localtime
import pytz

EU_TZ = pytz.timezone('Europe/Berlin')  # change to your actual EU timezone

from datetime import time

from datetime import time

def is_working_day(date_obj):
    return date_obj.weekday() < 5  # Monday = 0, Sunday = 6

def get_available_slots_for_date(date_obj, booked_times):
    all_slots = [time(14, 0), time(18, 0)]  # 2 PM and 6 PM
    return [slot for slot in all_slots if slot not in booked_times]

def is_working_day(date_obj):
    return date_obj.weekday() < 5  # Monday = 0, Sunday = 6

def get_available_slots_for_date(date_obj, booked_times):
    all_slots = [time(14, 0), time(18, 0)]  # 2 PM and 6 PM
    return [slot for slot in all_slots if slot not in booked_times]

    # Filter out already booked slots for that date
    booked_times = Appointment.objects.filter(preferred_date=date_obj).values_list('preferred_time', flat=True)

    # Remove booked slots
    available_slots = [slot for slot in slots if slot not in booked_times]
    return available_slots

def is_working_day(date_obj):
    # Monday=0, Sunday=6
    return date_obj.weekday() < 5


# utils.py


