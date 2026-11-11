from django.test import TestCase
from django.utils import timezone
from django.urls import reverse, resolve

from enquiry.views import contact_us, subscribe
from accounts.models import Account
from company.models import Company
from service.models import Service
from enquiry.models import Lead, Newsletter, channel_chioce


def url_with_args(name, args):
    return reverse(name, args=[args])


class TestUrls(TestCase):

    def setUp(self):
        self.user      = Account.objects.create_user(
            first_name = 'first',
            last_name  = 'last',
            email      = 'user1@example.com',
            password   = 'testpass1234',
            username   = 'first_last'
        )
        self.test_company   = Company.objects.create(
            company_name    = 'testcompany',
            website_address = 'http://testcompany.com',
            email           = 'test@testcompany.com',
            address_line_1  = 'address line 1',
            city            = 'test city',
            state           = 'test state',
            postal_code     = '111222',
            country         = 'test country',
            phone_number    = '11122233344',
            user            = self.user
        )
        self.test_service   = Service.objects.create(
            company         = self.test_company,
            name    = 'Test name',
            slug            = 'test_name',
        )
        self.test_lead      = Lead.objects.create(
            full_name       = 'test full name',
            email           = 'test@testlead.com',
            phone_number    = '11234567890',
            company_name    = 'test company',
            job_title       = 'test job title',
            service         = self.test_service,
            channel         = channel_chioce[3][0],
            others          = 'test optional',
            message         = 'my test message'
        )
        self.test_newsletter = Newsletter.objects.create(
            email            = 'test@news;etter.com',
            full_name        = 'test full'
        )

    # Staff URL tests
    def test_contact_us_urls_resolves(self):
        url = reverse('contact_us')
        self.assertEqual(resolve(url).func, contact_us)

    # Contact URL tests
    def test_subscribe_urls_resolves(self):
        url = reverse('subscribe')
        self.assertEqual(resolve(url).func, subscribe)
