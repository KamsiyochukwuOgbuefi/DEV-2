from django import forms
from .models import Industry, IndustryProcess
from company.models import Company


class IndustryForm(forms.ModelForm):
    class Meta:
        model = Industry
        fields = ['company', 'name', 'slug', 'description', 'image']

    # Initialize form fields with placeholders and classes
    def __init__(self, company, *args, **kwargs):
        super(IndustryForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Industry Name',
            'description': 'Describe Industry',
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


class IndustryProcessForm(forms.ModelForm):
    class Meta:
        model = IndustryProcess
        fields = ['company', 'industry', 'name', 'description', 'image']

    # Initialize form fields with placeholders and classes
    def __init__(self, company, *args, **kwargs):
        super(IndustryProcessForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Process Name',
            'description': 'Describe Process',
            'image': 'Upload Image',
        }

        # Set custom queryset for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-control'

        # Set custom queryset for the 'Industry' field
        self.fields['industry'].empty_label = 'Select Industry'
        self.fields['industry'].widget.attrs['class'] = 'form-control'

        # Apply placeholders and classes for other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Specific attributes for the 'description' field
        self.fields['description'].widget.attrs['rows'] = 3
