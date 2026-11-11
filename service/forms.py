from django import forms
from .models import Service, ServiceProcess
from company.models import Company


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['company', 'name', 'slug', 'description', 'image']

    # Initialize form fields with placeholders and classes
    def __init__(self, company, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Service Name',
            'description': 'Describe Service',
            'image': 'Upload Image',
        }

        # Set custom queryset for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-control'

        # Set readonly and placeholder for the 'slug' field
        self.fields['slug'].widget.attrs['readonly'] = 'readonly'
        self.fields['slug'].widget.attrs['class'] = 'slug form-control'

        # Apply placeholders and classes for other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Specific attributes for the 'description' field
        self.fields['description'].widget.attrs['rows'] = 3


class ServiceProcessForm(forms.ModelForm):
    class Meta:
        model = ServiceProcess
        fields = ['company', 'service', 'name', 'description', 'image']

    # Initialize form fields with placeholders and classes
    def __init__(self, company, *args, **kwargs):
        super(ServiceProcessForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Process Name',
            'description': 'Describe Process',
            'image': 'Upload Image',
        }

        # Set custom queryset for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-control'

        # Set custom queryset for the 'service' field
        self.fields['service'].empty_label = 'Select Service'
        self.fields['service'].widget.attrs['class'] = 'form-control'

        # Apply placeholders and classes for other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Specific attributes for the 'description' field
        self.fields['description'].widget.attrs['rows'] = 3
