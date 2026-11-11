from django.test import TestCase
from company.models import Company, CompanyOverview

def create_company(
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
    logo='photos/logos/test_logo.png',
    is_client=True
):
    return Company.objects.create(
        company_name=company_name,
        website_address=website_address,
        email=email,
        address_line_1=address_line_1,
        address_line_2=address_line_2,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country,
        phone_number=phone_number,
        phone_number_2=phone_number_2,
        logo=logo,
        is_client=is_client,
    )

def create_company_overview(
    company,
    business_overview = 'test business overview',
    isms              = 'test ISMS',
    mission           = 'test mission statement',
    vision            = 'test vision',
    values            = 'test values'
):
    return CompanyOverview.objects.create(
        company=company,
        business_overview = business_overview,
        isms = isms,
        mission = mission,
        vision = vision,
        values = values
    )

class TestModels(TestCase):

    def test_create_company(self):
        company_name = 'testcompany'
        email = 'test@testcompany.com'

        # Create a company instance
        company = create_company()

        # Assert string representation and field correctness
        self.assertEqual(str(company), company_name)
        self.assertEqual(company.email, email)

    def test_create_company_overview(self):
        company_name = 'testcompany'
        business_overview = 'test business overview'

        # Create a company instance
        company = create_company()

        # Create a company overview instance
        company_overview = create_company_overview(company)

        # Assert string representation and field correctness
        self.assertEqual(str(company_overview), company_name)
        self.assertEqual(company_overview.business_overview, business_overview)
