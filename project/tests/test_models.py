from django.test import TestCase
from company.models import Company
from service.models import Service
from project.models import Project, ProjectImages, Partner, Testimonial

# Helper functions to create model instances
def create_company(
    company_name    = 'testcompany', 
    website_address = 'http://testcompany.com',
    email           = 'test@testcompany.com', 
    address_line_1  = 'address line 1',
    city            = 'test city', 
    state           = 'test state', 
    postal_code     = 'test code',
    country         = 'test country', 
    phone_number    = 'testphone'
):
    return Company.objects.create(
        company_name    = company_name, 
        website_address = website_address,
        email           = email, 
        address_line_1  = address_line_1, 
        city            = city,
        state           = state, 
        postal_code     = postal_code, 
        country         = country, 
        phone_number    = phone_number
    )

def create_service(
    company, 
    name            = 'Testing Service', 
    description     = 'Testing service description'
):
    return Service.objects.create(
        company             = company, 
        name                = name, 
        description         = description
    )

def create_project(
    company, 
    service, 
    title         = 'Test Project Title', 
    project_scope = 'Test Project Scope', 
    project_url   = 'http://testproject.com'
):
    return Project.objects.create(
        company       = company, 
        service       = service, 
        title         = title, 
        project_scope = project_scope, 
        project_url   = project_url
    )

def create_project_image(
    company, 
    service, 
    project, 
    name        = 'Test image', 
    description = 'Test image description'
):
    return ProjectImages.objects.create(
        company     = company, 
        service     = service, 
        project     = project, 
        name        = name, 
        description = description
    )

def create_partner(company, name = 'Test Partner'):
    return Partner.objects.create(
        company = company, 
        name    = name
    )

def create_testimonial(
    company, 
    name         = 'Test User', 
    content      = 'This is a great service!', 
    company_name = 'Test Company', 
    location     = 'Test Location'
):
    return Testimonial.objects.create(
        company      = company, 
        name         = name, 
        content      = content, 
        company_name = company_name, 
        location     = location
    )
