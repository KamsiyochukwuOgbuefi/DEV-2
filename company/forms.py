from django import forms
from .models import Company, CompanyOverview

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'company_name', 'website_address', 'email', 'address_line_1', 
            'address_line_2', 'city', 'state', 'phone_number', 'phone_number_2',
            'postal_code', 'country', 'logo',
        ]

    # Initialize form fields with placeholders and classes
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        placeholders = {
            'company_name': 'Enter Company Name',
            'website_address': 'Enter Website Address',
            'email': 'Enter Email Address',
            'address_line_1': 'Enter Address Line 1',
            'address_line_2': 'Enter Address Line 2 (optional)',
            'city': 'Enter City',
            'state': 'Enter State',
            'phone_number': 'Enter Phone Number',
            'phone_number_2': 'Enter Second Phone Number (optional)',
            'postal_code': 'Enter Postal Code',
            'country': 'Enter Country',
            'logo': 'Upload Logo',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

class CompanyOverviewForm(forms.ModelForm):
    class Meta:
        model = CompanyOverview
        fields = [
            'company', 'vision', 'mission', 'values', 
            'business_overview', 'goals',
        ]

    def __init__(self, *args, **kwargs):
        super(CompanyOverviewForm, self).__init__(*args, **kwargs)
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].widget.attrs['class'] = 'form-control'
        
        placeholders = {
            'mission': 'Enter Mission Statement',
            'vision': 'Enter Vision Statement',
            'values': 'Enter Values',
            'business_overview': 'Enter Business Overview',
            'goals': 'Enter Goals',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['rows'] = 3
