from django.test import TestCase
from company.models import Company
from service.models import Service, ServiceProcess
from accounts.models import Account

def create_company(
    company_name    = 'test company',
    website_address = 'http://testcompany.com',
    email           = 'test@testcompany.com',
    address_line_1  = 'address line 1',
    city            = 'test city',
    state           = 'test state',
    postal_code     = 'test code',
    country         = 'test country',
    phone           = 'testphone'
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
        phone           = phone
    )

def create_service(
    company,
    name                = 'test service',
    slug                = 'test_service',
    description         =  'my test service'
):
    return Service.objects.create(
        company              = company,
        name                 = name,
        slug                 = slug,
        description          = description
    )

def create_service_process(
    company,
    service,
    name                = 'test process',
    description         = 'my test process'
):
    return ServiceProcess.objects.create(
        company              = company,
        service              = service,
        name                 = name,
        description          = description
    )
