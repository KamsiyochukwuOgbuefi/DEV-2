from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from company.models import Company
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Industry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='photos/industries', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Automatically generates a slug from the industry_name before saving the instance to the database
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def update_url(self):
        return reverse('update_industry', args=[self.id])

    def delete_url(self):
        return reverse('delete_industry', args=[self.id])

    def industry_url(self):
        return reverse('industry_slug', args=[self.slug])

    class Meta:
        verbose_name = 'Industry'
        verbose_name_plural = 'Industries'

    def __str__(self):
        return self.name

class IndustryProcess(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, default='1')
    industry = ChainedForeignKey(
        Industry,
        chained_field="company",
        chained_model_field="company",
        show_all=False,
        auto_choose=True,
        default=None)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='photos/industry_process', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def update_url(self):
        return reverse('update_industry_process', args=[self.id])

    def delete_url(self):
        return reverse('delete_industry_process', args=[self.id])

    class Meta:
        verbose_name = 'Industry Process'
        verbose_name_plural = 'Industry Processes'

    def __str__(self):
        return self.name

