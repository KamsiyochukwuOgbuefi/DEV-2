import io
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from accounts.models import Account
from company.models import Company
from service.models import Service
from project.models import Project, ProjectImages, Partner, Testimonial
from project.forms import ProjectForm, ProjectImageForm, PartnerForm, TestimonialForm
import datetime  # Ensure datetime is imported
from django.utils import timezone


def generate_photo_file():
    file              = io.BytesIO()
    image             = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name         = 'test_image.png'
    file.seek(0)
    return file


class TestForms(TestCase):

    def setUp(self):
        self.user         = Account.objects.create_user(
            first_name      = 'first',
            last_name       = 'last',
            email           = 'user1@example.com',
            password        = 'testpass1234',
            username        = 'first_last'
        )
        self.test_company = Company.objects.create(
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
        self.test_service = Service.objects.create(
            company         = self.test_company,
            name            = 'test service',
            slug            = 'test_service',
            description     = 'my test service'
        )

        self.test_project = Project.objects.create(
            company         = self.test_company,
            service         = self.test_service,
            title           = 'Test Project',
            project_scope   = 'Project Scope',
            project_url     = 'http://projecturl.com',
            completion_date = timezone.make_aware(datetime.datetime(2025, 1, 1))
        )

        # Create test project image
        photo_file              = generate_photo_file()
        self.test_project_image = ProjectImages.objects.create(
            company             = self.test_company,
            service             = self.test_service,
            project             = self.test_project,
            image               = SimpleUploadedFile(photo_file.name, photo_file.read(), content_type='image/png'),
            name                = 'Test Image',
            description         = 'Test Image Description'
        )


        # Create test project image
        photo_file          = generate_photo_file()
        self.test_partner   = Partner.objects.create(
            company         = self.test_company,
            name            = 'Test Partner',
            image           = SimpleUploadedFile(photo_file.name, photo_file.read(), content_type='image/png')
        )

        self.test_testimonial = Testimonial.objects.create(
            company         = self.test_company,
            name            = 'Test Client',
            content         = 'Testimonial content',
            company_name    = 'Test Company Name',
            location        = 'Test Location'
        )

    def test_project_form_valid_data(self):
        data = {
            'company'       : self.test_company.id,
            'service'       : self.test_service.id,
            'title'         : 'Test Project Title',
            'project_scope' : 'Scope of Test Project',
            'project_url'   : 'http://testproject.com',
            'completion_date': timezone.make_aware(datetime.datetime(2025, 1, 1))
        }

        form = ProjectForm(self.test_company, data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_project_form_no_data(self):
        form = ProjectForm(self.test_company, data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)

    def test_project_image_form_valid_data(self):
        photo_file = generate_photo_file()
        files = {'image': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company'       : self.test_company.id,
            'service'       : self.test_service.id,
            'project'       : self.test_project.id,
            'name'          : 'Test Image Name',
            'description'   : 'Test Image Description'
        }

        form = ProjectImageForm(self.test_company, data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_project_image_form_no_data(self):
        form = ProjectImageForm(self.test_company, data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)

    def test_partner_form_valid_data(self):
        photo_file = generate_photo_file()
        files = {'image': SimpleUploadedFile(photo_file.name, photo_file.read())}

        data = {
            'company'       : self.test_company.id,
            'name'          : 'Test Partner',
        }

        form = PartnerForm(self.test_company, data, files)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_partner_form_no_data(self):
        form = PartnerForm(self.test_company, data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_testimonial_form_valid_data(self):
        data = {
            'company'      : self.test_company.id,
            'name'         : 'Test Client',
            'content'      : 'This is a testimonial content',
            'company_name' : 'Test Company',
            'location'     : 'Test Location'
        }

        form = TestimonialForm(self.test_company, data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_testimonial_form_no_data(self):
        form = TestimonialForm(self.test_company, data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
