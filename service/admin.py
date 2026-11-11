from django.contrib import admin
from .models import Service, ServiceProcess

# Register your models here.
class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'created_date', 'modified_date')

class ServiceProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'created_date', 'modified_date')


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceProcess, ServiceProcessAdmin)
