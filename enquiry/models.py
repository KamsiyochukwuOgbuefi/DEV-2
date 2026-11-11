from django.db import models
from django.core.validators import RegexValidator
from service.models import Service

# Validator for phone number
phone_number_validator = RegexValidator(r'^\+?[0-9]*$', 'Only numeric values are allowed.')

# Create your models here.
channel_chioce = (
    (0,'Select How you heard about us'),
    ('Facebook','Facebook'),
    ('Instagram', 'Instagram'),
    ('Google','Google'),
    ('word of mouth','Word of Mouth'),
    ('youtube','Youtube'),
    ('Tiktok','Tiktok'),
    ('Marketer','Marketer'),
    ('others','Others'),
)


class Lead(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number    = models.CharField(max_length=20, null=True, blank=True, validators=[phone_number_validator])
    company_name = models.CharField(max_length=50,  blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True,)
    channel = models.CharField(max_length=100, choices=channel_chioce, default=0)
    others = models.CharField(max_length=50,  blank=True)
    message = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

class Newsletter(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.email
