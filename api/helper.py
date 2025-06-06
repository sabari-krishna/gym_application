# File: api/helper.py

import pytz
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from api.models import FitnessClass, Booking, User


# Clear existing data
Booking.objects.all().delete()
FitnessClass.objects.all().delete()
User.objects.exclude(is_superuser=True).delete()

# Create test classes
now = datetime.now(pytz.timezone("Asia/Kolkata"))

classes = [
    FitnessClass.objects.create(
        name="Yoga",
        instructor="Priya",
        datetime_ist=now + timedelta(days=1, hours=7),
        available_slots=5
    ),
    FitnessClass.objects.create(
        name="HIIT",
        instructor="Arjun",
        datetime_ist=now + timedelta(days=2, hours=8),
        available_slots=3
    ),
    FitnessClass.objects.create(
        name="Zumba",
        instructor="Meera",
        datetime_ist=now + timedelta(days=3, hours=9),
        available_slots=2
    ),
]

print("Injected test data:")
print(f"  Classes: {FitnessClass.objects.count()}")
