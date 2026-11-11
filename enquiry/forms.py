from django import forms
from .models import Lead, Newsletter

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'full_name', 'email', 'phone_number', 'company_name', 
            'job_title', 'channel', 'service', 'others', 'message'
        ]

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Enter Full Name',
            'email': 'Enter Email Address',
            'phone_number': 'Enter Phone Number',
            'company_name': 'Enter Company Name',
            'job_title': 'Enter Job Title',
            'service': 'Select Service You Are Interested In',
            'channel': 'Select How You Heard About Us',
            'others': 'If others, please specify',
            'message': 'Enter Message',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Add blank choice for the 'service' field
        self.fields['service'].empty_label = "Select Service You Are Interested In"

        # Custom attributes for specific fields
        self.fields['channel'].widget.attrs['class'] = 'form-select'
        self.fields['message'].widget.attrs['rows'] = 4

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email', 'full_name']

    # Initialize form fields with placeholders and classes
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        placeholders = {
            'email': 'Enter Email Address',
            'full_name': 'Enter Full Name (optional)',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
