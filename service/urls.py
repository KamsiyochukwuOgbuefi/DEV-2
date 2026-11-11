from django.urls import path
from . import views

urlpatterns = [
    path('services/<slug:slug>/', views.service, name='service_slug'),
    path('service_dashboard/', views.service_dashboard, name='service_dashboard'),
    path('update_service/<int:id>', views.update_service, name='update_service'),
    path('delete_service/<int:id>', views.delete_service, name='delete_service'),
    path('service_process_dashboard/', views.service_process_dashboard, name='service_process_dashboard'),
    path('update_service_process/<int:id>', views.update_service_process, name='update_service_process'),
    path('delete_service_process/<int:id>', views.delete_service_process, name='delete_service_process'),
]
