from django.contrib import admin
from .models import FAQQuestion, FAQCategory

# Register your models here.
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20


class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ('category', 'question', 'answer')
    list_filter = ('category',)
    search_fields = ('question', 'answer')
    list_per_page = 20
    autocomplete_fields = ('category',)  # Provides autocomplete for the category field
    

admin.site.register(FAQCategory, FAQCategoryAdmin)
admin.site.register(FAQQuestion, FAQQuestionAdmin)
