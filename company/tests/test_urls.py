from django.test import TestCase
from django.urls import reverse, resolve
from company.views import company, company_dashboard, business_overview

from company.models import Company, CompanyOverview
from accounts.models import Account


def url_with_args(name, args):
    return reverse(name, args=[args])

class TestUrls(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )

        # Create a company
        self.test_company = Company.objects.create(
            id=1,
            company_name='testcompany',
            website_address='http://testcompany.com',
            email='test@testcompany.com',
            address_line_1='address line 1',
            address_line_2='address line 2',
            city='test city',
            state='test state',
            postal_code='test code',
            country='test country',
            phone_number='+123456789',
            phone_number_2='9876543210',
            is_client=True,
            user=self.user
        )

        # Create a company overview
        self.test_company_overview = CompanyOverview.objects.create(
            company           = self.test_company,
            business_overview = 'test business overview',
            isms              = 'test ISMS',
            mission           = 'test mission statement',
            vision            = 'test vision',
            values            = 'test values'
        )

    def test_company_urls_resolves(self):
        url = reverse('company')
        self.assertEqual(resolve(url).func, company)

    def test_company_dashboard_urls_resolves(self):
        url = reverse('company_dashboard')
        self.assertEqual(resolve(url).func, company_dashboard)

    def test_business_overview_urls_resolves(self):
        url = reverse('business_overview')
        self.assertEqual(resolve(url).func, business_overview)

