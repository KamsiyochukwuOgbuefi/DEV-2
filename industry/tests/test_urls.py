from django.test import TestCase
from django.urls import reverse, resolve
from industry.views import (
   industry, industry_dashboard, update_industry, delete_industry, industry_process_dashboard, 
   update_industry_process, delete_industry_process
)
from accounts.models import Account
from company.models import Company
from industry.models import (
    Industry, IndustryProcess,
)

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def url_with_args(name, args):
    return reverse(name, args=[args])

class TestUrls(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            first_name    = 'first',
            last_name     = 'last',
            email         = 'user1@example.com',
            password      = 'testpass1234',
            username      = 'first_last'
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
        self.test_industry = Industry.objects.create(
            company             = self.test_company,
            name                = 'test industry',
            slug                = 'test_industry',
            description         =  'my test industry'
        )
        self.test_industry_process = IndustryProcess.objects.create(
            company               = self.test_company,
            industry              = self.test_industry,
            name                  = 'test process',
            description           = 'my test process'
        )

    def test_industry_urls_resolves(self):
        url = url_with_args('industry_slug', self.test_industry.slug)
        self.assertEqual(resolve(url).func, industry)

    def test_industry_dashboard_urls_resolves(self):
        url = reverse('industry_dashboard')
        self.assertEqual(resolve(url).func, industry_dashboard)

    def test_update_industry_urls_resolves(self):
        url = url_with_args('update_industry', self.test_industry.id)
        self.assertEqual(resolve(url).func, update_industry)

    def test_delete_industry_urls_resolves(self):
        url = url_with_args('delete_industry', self.test_industry.id)
        self.assertEqual(resolve(url).func, delete_industry)

    def test_industry_process_dashboard_urls_resolves(self):
        url = reverse('industry_process_dashboard')
        self.assertEqual(resolve(url).func, industry_process_dashboard)

    def test_update_industry_process_urls_resolves(self):
        url = url_with_args('update_industry_process', self.test_industry.id)
        self.assertEqual(resolve(url).func, update_industry_process)

    def test_delete_industry_process_urls_resolves(self):
        url = url_with_args('delete_industry_process', self.test_industry.id)
        self.assertEqual(resolve(url).func, delete_industry_process)

