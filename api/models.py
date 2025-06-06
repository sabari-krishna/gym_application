import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# Custom User Model
class User(AbstractUser):
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

#Fitness class model - ZUMBA, YOGA, HIIT
class FitnessClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    datetime_ist = models.DateTimeField()
    available_slots = models.PositiveIntegerField()

    def datetime_utc(self):
        import pytz
        ist = pytz.timezone("Asia/Kolkata")
        dt = self.datetime_ist

        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            dt = ist.localize(dt)
        return dt.astimezone(pytz.utc)

    def __str__(self):
        return f"{self.name} with {self.instructor} at {self.datetime_ist}"

#Booking model
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)