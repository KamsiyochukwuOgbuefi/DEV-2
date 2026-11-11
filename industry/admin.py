from django.contrib import admin
from .models import Industry, IndustryProcess

# Register your models here.
class IndustryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'created_date', 'modified_date')

class IndustryProcessAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'created_date', 'modified_date')


admin.site.register(Industry, IndustryAdmin)
admin.site.register(IndustryProcess, IndustryProcessAdmin)
