from django import forms
from .models import Staff
from company.models import Company


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'company', 'first_name', 'last_name', 'position', 
            'image', 'description', 'is_active', 
            'is_management', 'is_primary_contact'
        ]

    # Initialize form fields with placeholders and classes
    def __init__(self, company, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Enter First Name',
            'last_name': 'Enter Last Name',
            'position': 'Enter Position',
            'description': 'Provide a brief description',
            'image': 'Upload Image',
        }

        # Set custom queryset and attributes for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-control'

        # Apply placeholders and classes to other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Specific attributes for the 'description' field
        self.fields['description'].widget.attrs['rows'] = 3

        # Boolean fields
        for field in ('is_active', 'is_management', 'is_primary_contact'):
            self.fields[field].widget.attrs['class'] = 'form-check-input'
