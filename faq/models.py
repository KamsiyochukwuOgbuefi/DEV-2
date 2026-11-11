from django.urls import reverse
from django.db import models
from service.models import Service, ServiceProcess  # Import Service and ServiceProcess models

class FAQCategory(models.Model):
    home_note = models.TextField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def update_url(self):
        return reverse('update_faqcategory', args=[self.id])

    def delete_url(self):
        return reverse('delete_faqcategory', args=[self.id])

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'FAQCategory'
        verbose_name_plural = 'FAQCategories'

class FAQQuestion(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE)
    question = models.TextField(max_length=1000)
    answer = models.TextField(max_length=2000)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    def get_url(self):
        return reverse('faq_detail', args=[str(self.category.id)])

    def update_url(self):
        return reverse('update_faqquestion', args=[self.id])
    
    def delete_url(self):
        return reverse('delete_faqquestion', args=[self.id])
    
    class Meta:
        verbose_name = 'FAQQuestion'
        verbose_name_plural = 'FAQQuestions'
