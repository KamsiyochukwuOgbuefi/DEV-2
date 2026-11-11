from django.db import models
from company.models import Company
from django.urls import reverse

# Create your models here.
class Staff(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/staffs', blank=True, null=True)
    description = models.TextField(max_length=500)
    is_active = models.BooleanField(default=True)
    is_management = models.BooleanField(default=False)
    is_primary_contact = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def update_url(self):
        return reverse('update_staff', args=[self.id])

    def delete_url(self):
        return reverse('delete_staff', args=[self.id])

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staffs'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self): 
        return self.first_name
    