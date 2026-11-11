from django.urls import path
from . import views  # Assuming these views are in the current app

urlpatterns = [
    # Project-related URLs
    path('project/<int:project_id>/', views.project, name='project'),
    path('service/<slug:service_slug>/projects/', views.service_projects, name='service_projects'),
    path('dashboard/projects/', views.project_dashboard, name='project_dashboard'),
    path('dashboard/projects/update/<int:id>/', views.update_project, name='update_project'),
    path('dashboard/projects/delete/<int:id>/', views.delete_project, name='delete_project'),

    
    # Project-image-related URLs
    path('dashboard/projects-image/', views.project_image_dashboard, name='project_image_dashboard'),
    path('dashboard/projects/update-image/<int:id>/', views.update_project_image, name='update_project_image'),
    path('dashboard/projects/delete-image/<int:id>/', views.delete_project_image, name='delete_project_image'),
    
    # Partner-related URLs
    path('dashboard/partners/', views.partner_dashboard, name='partner_dashboard'),
    path('dashboard/partners/update/<int:id>/', views.update_partner, name='update_partner'),
    path('dashboard/partners/delete/<int:id>/', views.delete_partner, name='delete_partner'),
    
    # Testimonial-related URLs
    path('testimonials/', views.testimonial, name='testimonial'),
    path('dashboard/testimonials/', views.testimonial_dashboard, name='testimonial_dashboard'),
    path('dashboard/testimonials/update/<int:id>/', views.update_testimonial, name='update_testimonial'),
    path('dashboard/testimonials/delete/<int:id>/', views.delete_testimonial, name='delete_testimonial'),
]
