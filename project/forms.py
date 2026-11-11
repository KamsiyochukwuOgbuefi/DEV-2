from django import forms
from .models import Project, ProjectImages, Partner, Testimonial
from company.models import Company


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'company', 'service', 'title', 
            'project_scope', 'project_url', 
            'completion_date'
        ]

    def __init__(self, company, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        placeholders = {
            'title': 'Enter Project Title',
            'project_scope': 'Describe the project scope',
            'project_url': 'Provide project URL (optional)',
        }

        # Set custom queryset and attributes for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-select'

        # Set custom queryset and attributes for the 'service' field
        self.fields['service'].empty_label = 'Select Service'
        self.fields['service'].widget.attrs['class'] = 'form-select'

        # Apply placeholders and classes to other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Specific attributes for the 'project_scope' field
        self.fields['project_scope'].widget.attrs['rows'] = 5

        # Custom attributes for 'completion_date'
        self.fields['completion_date'].widget.attrs['class'] = 'form-control'
        self.fields['completion_date'].widget.input_type = 'date'


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImages
        fields = [
            'company', 'service', 
            'project', 'image', 
            'name', 'description'
        ]

    def __init__(self, company, *args, **kwargs):
        super(ProjectImageForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Image Name',
            'description': 'Describe the image',
        }

        # Set custom queryset and attributes for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-select'

        # Set custom queryset and attributes for the 'service' field
        self.fields['service'].empty_label = 'Select Service'
        self.fields['service'].widget.attrs['class'] = 'form-select'

        # Set custom queryset and attributes for the 'project' field
        self.fields['project'].empty_label = 'Select Project'
        self.fields['project'].widget.attrs['class'] = 'form-select'

        # Apply placeholders and classes to other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Specific attributes for the 'description' field
        self.fields['description'].widget.attrs['rows'] = 5

        # Custom attributes for 'image'
        self.fields['image'].widget.attrs['class'] = 'form-control-file'


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ['company', 'image', 'name']

    def __init__(self, company, *args, **kwargs):
        super(PartnerForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Partner Name',
        }

        # Set custom queryset and attributes for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-select'

        # Apply placeholders and classes to other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Custom attributes for 'image'
        self.fields['image'].widget.attrs['class'] = 'form-control-file'


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['company', 'name', 'content', 'company_name', 'location']

    def __init__(self, company, *args, **kwargs):
        super(TestimonialForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Client Name',
            'content': 'Enter Testimonial Content',
            'company_name': 'Enter Company Name',
            'location': 'Enter Location',
        }

        # Set custom queryset and attributes for the 'company' field
        self.fields['company'].empty_label = 'Select Company'
        self.fields['company'].queryset = Company.objects.filter(id=company.id)
        self.fields['company'].widget.attrs['class'] = 'form-control'

        # Apply placeholders and classes to other fields
        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Specific attributes for 'content'
        self.fields['content'].widget.attrs['rows'] = 3
