import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from accounts.models import Account
from company.models import Company
from industry.models import Industry, IndustryProcess
from industry.forms import IndustryForm, IndustryProcessForm

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_image.png'
    file.seek(0)
    return file


class TestForms(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            first_name  = 'first',
            last_name   = 'last',
            email       = 'user1@example.com',
            password    = 'testpass1234',
            username    = 'first_last'
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
        self.companies =self.test_company # Pass a single instance, not a queryset

        self.test_industry_process = IndustryProcess.objects.create(
            company             = self.test_company,
            industry             = self.test_industry,
            name                = 'test process',
            description         = 'my test process'
        )

    def test_industry_form_valid_data(self):

        photo_file = generate_photo_file()
        files = {'image': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company'               : self.test_company.id,
            'name'                  : 'test industry two',
            'slug'                  : 'test_industry_two',
            'description'           : 'my test industry'
        }

        form = IndustryForm(self.companies, data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_industry_form_no_data(self):
        form = IndustryForm(self.companies, data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_industry_process_form_valid_data(self):

        photo_file = generate_photo_file()
        files = {'image': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company'               : self.test_company.id,
            'industry'               : self.test_industry.id,
            'name'                  : 'test process name',
            'description'           : 'test process description'
        }

        form = IndustryProcessForm(self.companies, data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_industry_process_form_no_data(self):
        form = IndustryProcessForm(self.companies, data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
