import io
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.base import ContentFile
from accounts.models import Account
from company.models import Company, CompanyOverview
from PIL import Image
from django.conf import settings
import os


def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_logo.png'
    file.seek(0)
    return file


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.company_url = reverse('company')
        self.company_dashboard_url = reverse('company_dashboard')
        self.BO_url = reverse('business_overview')
        self.admin_login_url = reverse('admin_login')

        # Create a user to associate with the company
        self.user = Account.objects.create_user(
            first_name='first',
            last_name='last',
            email='user1@example.com',
            password='testpass1234',
            username='first_last'
        )
        self.user.is_admin = True  # Manually set `is_admin`
        self.user.is_active = True
        self.user.save()

        # Create a company
        self.logo_file = generate_photo_file()
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
            phone_number_2='+9876543210',
            logo=ContentFile(self.logo_file.read(), 'test_logo.png'),
            is_client=True,
            user=self.user,
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

    def test_company(self):
        res = self.client.get(self.company_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/about_us.html')

    def test_company_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.company_dashboard_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/company_dashboard.html')

    def test_company_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        # Simulate a POST request to update company details
        photo_file = generate_photo_file()
        res = self.client.post(self.company_dashboard_url, {
            'company_name': 'updatedcompany',
            'website_address': 'http://updatedcompany.com',
            'email': 'updated@testcompany.com',
            'address_line_1': 'new address line 1',
            'address_line_2': 'new address line 2',
            'city': 'new city',
            'state': 'new state',
            'postal_code': '654321',
            'country': 'new country',
            'phone_number': '+987654321',
            'phone_number_2': '+9876543210',
            'logo': photo_file,
        }, format='multipart')

        self.assertEqual(res.status_code, 302)

        # Retrieve the updated Company instance
        updated_company = Company.objects.get(email='updated@testcompany.com')

        # Check whether the Company details are updated successfully
        self.assertEqual(updated_company.company_name, 'updatedcompany')
        self.assertEqual(updated_company.website_address, 'http://updatedcompany.com')

        # Check the redirection
        self.assertRedirects(res, self.company_dashboard_url)

    def test_BO_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.BO_url)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'company/business_overview.html')

    def test_BO_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        # Ensure the admin user is logged in
        admin_login_res = self.client.post(self.admin_login_url, {
            'email': 'user1@example.com',
            'password': 'testpass1234'
        })

        # Simulate a POST request to update business overview
        res = self.client.post(self.BO_url, {
            'company': self.test_company.id,
            'business_overview': 'test overview',
            'ISMS': 'test ISMS',
            'mission': 'test mission',
            'vision': 'test vision',
            'values': 'test values'
        })

        # Check the status code and redirection
        self.assertEqual(res.status_code, 302)

        # Check if the data is updated in the database
        updated_company_overview = CompanyOverview.objects.get(company=self.test_company)
        self.assertEqual(updated_company_overview.vision, 'test vision')

        # Check the redirection
        self.assertRedirects(res, self.BO_url)

    def test_non_admin_user_access(self):
        # Create a client user
        self.user = Account.objects.create_user(
            first_name='first',
            last_name='last',
            email='nonadmin@example.com',
            password='testpass1234',
            username='test first_last'
        )

        self.user.is_admin = False  # Set 'is_admin' to False to make the user a client
        self.user.is_active = True  # Set 'is_active' to True
        self.user.save()

        # Try to access the company dashboard view as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        res_dashboard = self.client.get(self.company_dashboard_url)

        # Check that the client is redirected to the login page after attempting to access the company dashboard
        self.assertEqual(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.company_dashboard_url))  # Ensure not redirected to company dashboard view

        # Try to access the business operations view as a client
        res_bo = self.client.get(self.BO_url)

        # Check that the client is redirected to the login page when attempting to access business operations view
        self.assertEqual(res_bo.status_code, 302)
        self.assertFalse(res_bo.url.startswith(self.BO_url))  # Ensure not redirected to business operations view


def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    files = [i for i in os.listdir(images_path)
             if os.path.isfile(os.path.join(images_path, i))
             and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))
