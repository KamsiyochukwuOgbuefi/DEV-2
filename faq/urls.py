from django.urls import path
from . import views

urlpatterns = [
    path('', views.faq, name='faq'),
    # path('faq/', views.faq_question, name='faq_categories'),
    path('question/<int:id>/', views.faq_question, name='faq_question'),
    path('faqcategory_dashboard/', views.faqcategory_dashboard, name='faqcategory_dashboard'),
    path('delete_faqcategory/<int:id>', views.delete_faqcategory, name='delete_faqcategory'),
    path('update_faqcategory/<int:id>', views.update_faqcategory, name='update_faqcategory'),
    path('faqquestion_dashboard/', views.faqquestion_dashboard, name='faqquestion_dashboard'),
    path('delete_faqquestion/<int:id>', views.delete_faqquestion, name='delete_faqquestion'),
    path('update_faqquestion/<int:id>', views.update_faqquestion, name='update_faqquestion'),
]

