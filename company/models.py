from django.core.validators import RegexValidator
from django.db import models
from accounts.models import Account
from django.urls import reverse

# Validator for phone number
phone_number_validator = RegexValidator(r'^\+?[0-9]*$', 'Only numeric values are allowed.')

# Create your models here.
class Company(models.Model):
    company_name = models.CharField(max_length=50)
    website_address = models.CharField(max_length=200)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    phone_number    = models.CharField(max_length=20, validators=[phone_number_validator]) 
    phone_number_2    = models.CharField(max_length=20, blank=True, null=True, validators=[phone_number_validator]) 
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=12)
    country = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='photos/logos')
    is_client = models.BooleanField(default=False)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def formatted_phone_number(self):
        """Format the phone number as '832-865-5849' with '+234' prefix."""
        if self.phone_number:
            num = self.phone_number[-10:]  # Get the last 10 digits
            return f"+234 {num[:3]}-{num[3:6]}-{num[6:]}"
        return None

    def formatted_phone_number_2(self):
        """Format the second phone number if available."""
        if self.phone_number_2:
            num = self.phone_number_2[-10:]
            return f"+1 {num[:3]}-{num[3:6]}-{num[6:]}"
        return None

    def address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def province(self):
        return f'{self.city} {self.state} {self.country}'

    def update_url(self):
        return reverse('update_company', args=[self.id])

    def delete_url(self):
        return reverse('delete_company', args=[self.id])

    # within the admin django pluralizes models by adding 's' to name
    # e.g. company = companys to correct this
    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'companies'

    def __str__(self):
        return self.company_name

class CompanyOverview(models.Model):
    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        unique=True,
    )
    mission = models.TextField(max_length=500, blank=True)
    vision = models.TextField(max_length=500, blank=True)
    values = models.TextField(max_length=500, blank=True)
    business_overview = models.TextField(max_length=1000, blank=True)
    goals = models.TextField(max_length=500, blank=True)
    id = models.AutoField(primary_key=True, default=None)

    def update_url(self):
        return reverse('update_business_overview', args=[self.company_id])

    def delete_url(self):
        return reverse('delete_business_overview', args=[self.company_id])

    def __str__(self):
        return self.company.company_name
    