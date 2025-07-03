from django.contrib import admin

# Register your models here.

from .models import Appointment, ConfusionType

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'preferred_date', 'preferred_time', 'state')
    list_filter = ('preferred_date', 'preferred_time', 'state')
    search_fields = ('name', 'email', 'phone','payment_status','preferred date','preferred_time')
    fields = (
        'name',
        'email',
        'phone',
        'address',
        'city',
        'state',
        'visa_country',
        'agency_name',
        'preferred_date',
        'preferred_time',
        'confusions',
        'notes',
        'payment_status',
        'file',
        'reviewed',
        'status',
    )
    readonly_fields = ('submitted_at',)

admin.site.register(ConfusionType)

