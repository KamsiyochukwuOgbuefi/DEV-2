from django import forms
from .models import FAQCategory, FAQQuestion

class FAQCategoryForm(forms.ModelForm):
    class Meta:
        model = FAQCategory
        fields = ['name', 'home_note']

    # Initialize form fields with placeholders and classes
    def __init__(self, *args, **kwargs):
        super(FAQCategoryForm, self).__init__(*args, **kwargs)
        placeholders = {
            'name': 'Enter Category Name',
            'home_note': 'Enter Category Description',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

class FAQQuestionForm(forms.ModelForm):
    class Meta:
        model = FAQQuestion
        fields = ['category', 'question', 'answer']

    # Initialize form fields with placeholders and classes
    def __init__(self, *args, **kwargs):
        super(FAQQuestionForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Select Category'
        placeholders = {
            'question': 'Enter Question',
            'answer': 'Enter Answer',
        }

        for field, placeholder in placeholders.items():
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'

        # Set specific class for 'category' field
        self.fields['category'].widget.attrs['class'] = 'form-control'
