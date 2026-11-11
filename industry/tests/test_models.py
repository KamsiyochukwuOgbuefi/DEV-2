from django.test import TestCase
from company.models import Company
from industry.models import Industry, IndustryProcess
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

def create_industry(
    company,
    name                = 'test industry',
    slug                = 'test_industry',
    description         =  'my test industry'
):
    return Industry.objects.create(
        company              = company,
        name                 = name,
        slug                 = slug,
        description          = description
    )

def create_industry_process(
    company,
    industry,
    name                = 'test process',
    description         = 'my test process'
):
    return IndustryProcess.objects.create(
        company              = company,
        industry             = industry,
        name                 = name,
        description          = description
    )
