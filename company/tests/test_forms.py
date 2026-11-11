import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from company.forms import CompanyForm, CompanyOverviewForm
from accounts.models import Account
from company.models import Company, CompanyOverview


# Generate a sample image file
def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_image.png'
    file.seek(0)
    return file


class TestForms(TestCase):

    def setUp(self):
        # Create a test user
        self.user = Account.objects.create_user(
            first_name='first',
            last_name='last',
            email='user1@example.com',
            password='testpass1234',
            username='first_last'
        )

        # Create a test company
        self.test_company = Company.objects.create(
            company_name='testcompany',
            website_address='http://testcompany.com',
            email='test@testcompany.com',
            address_line_1='address line 1',
            address_line_2='address line 2',
            city='test city',
            state='test state',
            postal_code='111222',
            country='test country',
            phone_number='11122233344',
            phone_number_2='9876543210',
            logo=None,
            is_client=True
        )

    def test_company_form_valid_data(self):
        # Create a mock photo file for the logo field
        photo_file = generate_photo_file()
        files = {'logo': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company_name': 'testcompany2',
            'website_address': 'http://testcompany2.com',
            'email': 'test@testcompany2.com',
            'address_line_1': 'address line 1',
            'address_line_2': 'address line 2',
            'city': 'test city',
            'state': 'test state',
            'postal_code': '111222',
            'country': 'test country',
            'phone_number': '11122233344',
            'phone_number_2': '9876543210'
        }

        form = CompanyForm(data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_company_form_invalid_data(self):
        # Missing required fields (e.g., company_name and email)
        form = CompanyForm(data={})
        self.assertFalse(form.is_valid())
        self.assertGreater(len(form.errors), 0)

    def test_company_overview_form_valid_data(self):
        data = {
            'company': self.test_company.id,
            'business_overview': 'test overview',
            'ISMS': 'test ISMS',
            'mission': 'test mission',
            'vision': 'test vision',
            'values': 'test values'
        }

        form = CompanyOverviewForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_company_overview_form_invalid_data(self):
        # Missing required fields (e.g., goal and mission)
        form = CompanyOverviewForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)