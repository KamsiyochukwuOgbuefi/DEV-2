from django.urls import path
from . import views

urlpatterns = [
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('update_staff/<int:id>', views.update_staff, name='update_staff'),
    path('delete_staff/<int:id>', views.delete_staff, name='delete_staff'),
]
