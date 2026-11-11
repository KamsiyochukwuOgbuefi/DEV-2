from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from company.models import Company
from service.models import Service
from django.urls import reverse

# Create your models here.
class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all=False,
        auto_choose=True,
        default=None)
    title = models.CharField(max_length=100)
    project_scope = models.TextField(max_length=500)
    project_url = models.CharField(max_length=200, blank=True, null=True)
    completion_date = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('project', args=[self.id])

    def update_url(self):
        return reverse('update_project', args=[self.id])

    def delete_url(self):
        return reverse('delete_project', args=[self.id])

    def __str__(self):
        return self.title

class ProjectImages(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service = ChainedForeignKey(
        Service,
        chained_field="company",
        chained_model_field="company",
        show_all = False,
        auto_choose=True,
        default=None)
    project = models.ForeignKey(
        Project,
        related_name="project_images",
        on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/project')
    name = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=500)

    def update_url(self):
        return reverse('update_project_image', args=[self.id])

    def delete_url(self):
        return reverse('delete_project_image', args=[self.id])

    class Meta:
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    def __str__(self):
        return self.project.title

# Partners Model
class Partner(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/partners')
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def update_url(self):
        return reverse('update_partner', args=[self.id])

    def delete_url(self):
        return reverse('delete_partner', args=[self.id])

    def __str__(self):
        return self.name

# Testimonial Model
class Testimonial(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(max_length=500)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def update_url(self):
        return reverse('update_testimonial', args=[self.id])

    def delete_url(self):
        return reverse('delete_testimonial', args=[self.id])

    def __str__(self):
        return f"Testimonial by {self.name} from {self.company_name}"
