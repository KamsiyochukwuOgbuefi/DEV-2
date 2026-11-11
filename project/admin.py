from django.contrib import admin
from .models import Project, ProjectImages, Partner, Testimonial

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'service', 'created_date', 'completion_date', 'modified_date')
    list_filter = ['completion_date', 'company', 'service']
    search_fields = ['title', 'project_scope', 'company__name']  # Search by title, scope, and company name
    list_per_page = 20

class ProjectImagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'service', 'project')  # Added 'created_date' for completeness
    search_fields = ['name']  # Enable search for description and project title

# Partners Model Admin
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')

# Testimonial Model Admin
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ['name', 'location']
    search_fields = ['name', 'location']


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImages, ProjectImagesAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
