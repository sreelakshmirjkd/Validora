from django.db import models
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from datetime import time
import pytz
from django.utils import timezone
from pytz import timezone as pytz_timezone


from django.core.exceptions import ValidationError
from datetime import time


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __str__(self):
        return self.name



class ConfusionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

def upload_to(instance, filename):
    return f"appointment_uploads/{instance.email}_{filename}"





class Appointment(models.Model):
    ALLOWED_TIME_SLOTS = [time(14, 0), time(18, 0)]  # 2 PM & 6 PM EU time

    name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone = models.CharField(max_length=20, null=False)
    nationality = models.CharField(max_length=100, default='Indian')
    visa_country = models.CharField(max_length=100, null=False, blank=False)
    agency_name = models.CharField(max_length=200)
    confusions = models.ManyToManyField('ConfusionType', blank=False)
    notes = models.TextField(blank=True)
    
 
    address = models.CharField(max_length=255, blank=True, null=True)  
    city = models.CharField(max_length=100, null=False, blank=False) 

    STATE = (
    ('NA','Select'),   
    ('AN', 'Andaman and Nicobar Islands'),
    ('AP', 'Andhra Pradesh'),
    ('AR', 'Arunachal Pradesh'),
    ('AS', 'Assam'),
    ('BR', 'Bihar'),
    ('CH', 'Chandigarh'),
    ('CT', 'Chhattisgarh'),
    ('DL', 'Delhi'),
    ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('GA', 'Goa'),
    ('GJ', 'Gujarat'),
    ('HP', 'Himachal Pradesh'),
    ('HR', 'Haryana'),
    ('JH', 'Jharkhand'),
    ('JK', 'Jammu and Kashmir'),
    ('KA', 'Karnataka'),
    ('KL', 'Kerala'),
    ('LA', 'Ladakh'),
    ('LD', 'Lakshadweep'),
    ('MH', 'Maharashtra'),
    ('ML', 'Meghalaya'),
    ('MN', 'Manipur'),
    ('MP', 'Madhya Pradesh'),
    ('MZ', 'Mizoram'),
    ('NL', 'Nagaland'),
    ('OD', 'Odisha'),
    ('PB', 'Punjab'),
    ('PY', 'Puducherry'),
    ('RJ', 'Rajasthan'),
    ('SK', 'Sikkim'),
    ('TN', 'Tamil Nadu'),
    ('TG', 'Telangana'),
    ('TR', 'Tripura'),
    ('UP', 'Uttar Pradesh'),
    ('UT', 'Uttarakhand'),
    ('WB', 'West Bengal'),
    )

    state = models.CharField(max_length=2, choices=STATE, default='NA', null=False, blank=False)



    preferred_date = models.DateField()
    preferred_time = models.TimeField()

    consent_privacy_policy = models.BooleanField(default=True, null=False, blank=False)
    consent_terms_conditions = models.BooleanField(default=True, null=False,blank=False)

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )


    submitted_at = models.DateTimeField(auto_now_add=True)
    
    file = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Link to file on Drive"
    )
    
    reviewed = models.BooleanField(
        default=False,
        help_text="Has this appointment been reviewed?"
    )
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the appointment"
    )




    def clean(self):
        # 1. Check that preferred_date and preferred_time are provided
        if not self.preferred_date:
            raise ValidationError("Preferred date is required.")
        if not self.preferred_time:
            raise ValidationError("Preferred time is required.")

        # 2. Only allow 2 PM or 6 PM
        if self.preferred_time not in self.ALLOWED_TIME_SLOTS:
            raise ValidationError("Appointments are only allowed at 2:00 PM or 6:00 PM (EU time).")

        # 3. Only weekdays
        if self.preferred_date.weekday() >= 5:
            raise ValidationError("Appointments can only be booked on working days (Monday to Friday).")

        # 4. Prevent double booking
        conflict = Appointment.objects.filter(
            preferred_date=self.preferred_date,
            preferred_time=self.preferred_time
        ).exclude(pk=self.pk)

        if conflict.exists():
            raise ValidationError("This time slot is already booked.")

