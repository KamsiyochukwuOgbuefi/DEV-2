from django.urls import path
from . import views

urlpatterns = [
    path('industries/<slug:slug>/', views.industry, name='industry_slug'),
    path('industry_dashboard/', views.industry_dashboard, name='industry_dashboard'),
    path('update_industry/<int:id>', views.update_industry, name='update_industry'),
    path('delete_industry/<int:id>', views.delete_industry, name='delete_industry'),
    path('industry_process_dashboard/', views.industry_process_dashboard, name='industry_process_dashboard'),
    path('update_industry_process/<int:id>', views.update_industry_process, name='update_industry_process'),
    path('delete_industry_process/<int:id>', views.delete_industry_process, name='delete_industry_process'),
]
