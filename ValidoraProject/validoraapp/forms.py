from django import forms
from .models import Contact

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
