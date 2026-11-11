from django.test import TestCase
from company.models import Company
from service.models import Service
from enquiry.models import Lead, Newsletter, channel_chioce


def create_company(
    company_name = 'testcompany',
    website_address = 'http://testcompany.com',
    email = 'test@testcompany.com',
    address_line_1 = 'address line 1',
    city = 'test city',
    state = 'test state',
    postal_code = 'test code',
    country = 'test country',
    phone_number = 'testphone'
):
    return Company.objects.create(
        company_name = company_name,
        website_address = website_address,
        email = email,
        address_line_1 = address_line_1,
        city = city,
        state = state,
        postal_code = postal_code,
        country = country,
        phone_number = phone_number
    )

def create_service(company, name = 'Test name', slug = 'test_name'):
    return Service.objects.create(
        company = company,
        name = name,
        slug = slug
    )


def create_enquiry(
    service,
    full_name = 'test full',
    email = 'test@testlead.com',
    phone_number = '2348176334125',
    company_name = 'test company',
    job_title    = 'test job title',
    message = 'my test message',
    channel = channel_chioce[3][0]
):
    return Lead.objects.create(
        service = service,
        full_name = full_name,
        phone_number= phone_number,
        email = email,
        company_name = company_name,
        job_title = job_title,
        message = message,
        channel = channel
    )

def create_lead(
    full_name = 'test full',
    email = 'test@testlead.com'

):
    return Newsletter.objects.create(
        full_name = full_name,
        email = email
    )


class TestModels(TestCase):

    def test_create_enquiry(self):
        full_name = 'test full'
        email = 'test@testlead.com'
        channel = channel_chioce[3][0]

        company = create_company()
        service = create_service(company)
        enquiry = create_enquiry(service)

        self.assertEqual(str(enquiry), email)
        self.assertEqual(enquiry.full_name, full_name)
        self.assertEqual(enquiry.channel, channel)

    def test_create_lead(self):
        full_name = 'test full'
        email = 'test@testlead.com'

        lead = create_lead()

        self.assertEqual(str(lead), email)
        self.assertEqual(lead.full_name, full_name)
