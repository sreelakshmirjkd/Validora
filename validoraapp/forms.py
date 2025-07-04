from django import forms
from .models import Contact, Appointment, ConfusionType

from datetime import date, timedelta, time
from django import forms
from .models import Appointment
from datetime import time

from django.forms import ModelMultipleChoiceField


from datetime import datetime
from django.core.exceptions import ValidationError

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Name',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your Email',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Your Phone',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Describe the visa agency, job offer, education consultant, or visa-related service you want our second opinion on...',
                'class': 'form-control'
            }),
        }





class AppointmentForm(forms.ModelForm):



    TIME_CHOICES = [
        
        (time(14, 0), '2:00 PM'),
        (time(18, 0), '6:00 PM'),
    ]



    preferred_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'preferred_time'})

    )

    preferred_date = forms.DateField(
        input_formats=['%d-%m-%Y'],  # accept only DD-MM-YYYY input
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DD-MM-YYYY',
            'name': 'preferred_date',
            'id': 'preferred_date',
            'autocomplete': 'off',  # prevent browser autocomplete messing with format
        })
    )


    class Meta:
        model = Appointment
        fields = [
            'name',
            'email',
            'nationality',
            'phone',
            'address',
            'city',
            'state',
            'visa_country',
            'agency_name',
            'confusions',
            'notes',
            'preferred_date',
            'preferred_time',

        

            
        ]
                
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control input-font',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control input-font',
                'placeholder': 'example@mail.com'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control input-font',
                'readonly': 'readonly'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control input-font',
                'placeholder': 'XXXXXXXXXX'
            }),


            'address': forms.Textarea(attrs={
                'class': 'form-control input-font',
                'rows': 2,
                'placeholder': 'Your address (optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control input-font',
                'placeholder': 'Your city'
            }),
            'state': forms.Select(attrs={
                'class': 'form-control input-font'
            }),

            'visa_country': forms.TextInput(attrs={
                'class': 'form-control input-font',
                'placeholder': 'Country you applied to'
            }),
            'agency_name': forms.TextInput(attrs={
                'class': 'form-control input-font',
                'placeholder': 'The name of Agency'
            }),
            'preferred_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control input-font'
            }),
            'preferred_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control input-font'
            }),
            'confusions': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control input-font',
                'rows': 3,
                'placeholder': 'Additional notes'
            }),


        }


        

    def __init__(self, *args, **kwargs):
        available_times = kwargs.pop('available_times', None)
        super().__init__(*args, **kwargs)

        self.fields['nationality'].initial = 'Indian'
        self.fields['nationality'].disabled = True

        
        self.fields['phone'].widget.attrs.update({
            'placeholder': 'Enter 10-digit mobile number',
            'pattern': '[0-9]{10}',
            'title': 'Enter a 10-digit mobile number without country code'
        })

        # Set queryset for confusions explicitly
        self.fields['confusions'].queryset = ConfusionType.objects.all()

        # Set min date for preferred_date
        min_date = (date.today() + timedelta(days=3)).strftime('%d-%m-%Y')
        self.fields['preferred_date'].widget.attrs['min'] = min_date

        # Dynamically set preferred_time choices
        if available_times is not None:
            choices = [(t.strftime("%H:%M:%S"), t.strftime("%I:%M %p")) for t in available_times]
            self.fields['preferred_time'].choices = choices
        else:
            choices = [(t.strftime("%H:%M:%S"), t.strftime("%I:%M %p")) for t, _ in self.TIME_CHOICES]
            self.fields['preferred_time'].choices = choices



