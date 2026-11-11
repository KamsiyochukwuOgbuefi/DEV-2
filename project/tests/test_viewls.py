import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Account
from company.models import Company
from service.models import Service
from project.models import Project, ProjectImages, Partner, Testimonial
import datetime  # Ensure datetime is imported
from django.utils import timezone

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_project_image.png'
    file.seek(0)
    return file

def url_with_args(name, args):
    return reverse(name, args=[args])

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.project_dashboard_url = reverse('project_dashboard')
        self.project_image_dashboard_url = reverse('project_image_dashboard')
        self.partner_dashboard_url = reverse('partner_dashboard')
        self.testimonial_url = reverse('testimonial')
        self.testimonial_dashboard_url = reverse('testimonial_dashboard')
        self.admin_login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.admin_admin_login_url = reverse('admin_login')
        self.setUp_file = generate_photo_file()

        self.user         = Account.objects.create_user(
            first_name      = 'first',
            last_name       = 'last',
            email           = 'user1@example.com',
            password        = 'testpass1234',
            username        = 'first_last'
        )
        self.test_company = Company.objects.create(
            id              =  1, # Add this line to set the specific ID for the company
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
            project_url     = 'https://projecturl.com',
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
        self.update_project_url = reverse('update_project', args=[self.test_project.id])
        self.delete_project_url = reverse('delete_project', args=[self.test_project.id])
        self.update_project_image_url = reverse('update_project_image', args=[self.test_project_image.id])
        self.delete_project_image_url = reverse('delete_project_image', args=[self.test_project_image.id])
        self.update_partner_url = reverse('update_partner', args=[self.test_partner.id])
        self.delete_partner_url = reverse('delete_partner', args=[self.test_partner.id])
        self.update_testimonial_url = reverse('update_testimonial', args=[self.test_testimonial.id])
        self.delete_testimonial_url = reverse('delete_testimonial', args=[self.test_testimonial.id])




    def test_service_projects(self):
        res = self.client.get(url_with_args('service_projects', self.test_service.slug))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'project/service_projects.html')

    def test_project(self):
        res = self.client.get(url_with_args('project', self.test_project.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'project/project.html')

    def test_project_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        # Authenticate the user
        self.client.login(email='user1@example.com', password='testpass1234')

        # Perform the GET request
        res = self.client.get(self.project_dashboard_url)

        # Debugging: Print context and status
        # print(res.context)  # Debug context
        # print(res.status_code)  # Debug status code

        # Assertions
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'project/project_dashboard.html')


    def test_project_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        # Authenticate the user
        self.client.login(email='user1@example.com', password='testpass1234')

        res = self.client.post(self.project_dashboard_url, {
            'company': self.test_company.id,
            'service': self.test_service.id,
            'title': 'Test Project',
            'project_scope': 'project Scope',
            'project_url': 'https://projecturl.com',
            'completion_date': timezone.make_aware(datetime.datetime(2025, 1, 1)),
        })
        # print(res.context['form'].errors)
        project = Project.objects.all().first()

        self.assertEqual(res.status_code, 302)
        self.assertEqual(project.project_url, 'https://projecturl.com')
        self.assertRedirects(res, self.project_dashboard_url)

    def test_update_project__GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_project', self.test_project.id))
        print(res.context['form'].errors)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'project/project_dashboard.html')


    def test_update_project_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload = {
            'company': self.test_company.id,
            'service': self.test_service.id,
            'title': 'Test Project',
            'project_scope': 'Test project Scope',
            'project_url': 'https://www.testproject.test',
            'completion_date': timezone.make_aware(datetime.datetime(2025, 1, 1)),
        }

        res = self.client.post(
            url_with_args('update_project', self.test_project.id),
            payload
        )
        # print(res.context['form'].errors)

        self.assertEqual(res.status_code, 302)
        self.test_project.refresh_from_db()
        self.assertEqual(str(self.test_project), payload['title'])
        self.assertRedirects(res, self.project_dashboard_url)

    def test_delete_project(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('delete_project', self.test_project.id))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.project_dashboard_url)
        self.assertFalse(Project.objects.filter(id=self.test_project.id).exists())

    def test_project_image_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.project_image_dashboard_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'project/project_image_dashboard.html')

    def test_project_image_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        photo_file = generate_photo_file()

        res = self.client.post(self.project_image_dashboard_url, {
            'company': self.test_company.id,
            'service': self.test_service.id,
            'project': self.test_project.id,
            'image' : photo_file,
            'name' : 'Test image2',
            'description' : 'Test image description2'
        })
        # print(res.context['form'].errors)
        project_image = ProjectImages.objects.all()[1]

        self.assertEqual(res.status_code, 302)
        self.assertEqual(project_image.project.id, self.test_project.id)
        self.assertRedirects(res, self.project_image_dashboard_url)

    def test_update_project_image__GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_project_image', self.test_project_image.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'project/project_image_dashboard.html')


    def test_update_project_image_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload =  {
            'company': self.test_company.id,
            'service': self.test_service.id,
            'project': self.test_project.id,
            'image' : photo_file,
            'name' : 'Test image2',
            'description' : 'Test image description2'
        }
        # print(res.context['form'].errors)

        res = self.client.post(
            url_with_args('update_project_image', self.test_project_image.id),
            payload
        )
        # print(res.context['form'].errors)

        self.assertEqual(res.status_code, 302)
        self.test_project_image.refresh_from_db()
        self.assertEqual(self.test_project_image.name, payload['name'])
        self.assertRedirects(res, self.project_image_dashboard_url)

    def test_delete_project_image(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('delete_project_image', self.test_project_image.id))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.project_image_dashboard_url)
        self.assertFalse(ProjectImages.objects.filter(id=self.test_project_image.id).exists())

    def test_partner_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.partner_dashboard_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'partner/partner_dashboard.html')

    def test_partner_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        photo_file = generate_photo_file()

        res = self.client.post(self.partner_dashboard_url, {
            'company': self.test_company.id,
            'name' : 'Test Partner',
            'image' : photo_file
        })
        # print(res.context['form'].errors)
        partner = Partner.objects.all()[1]

        self.assertEqual(res.status_code, 302)
        self.assertEqual(partner.name, 'Test Partner')
        self.assertRedirects(res, self.partner_dashboard_url)

    def test_update_partner__GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.update_partner_url)
        print(res.context['form'].errors)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'partner/partner_dashboard.html')


    def test_update_partner_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload =  {
            'company': self.test_company.id,
            'name' : 'Test Partner',
            'image' : photo_file
        }
        # print(res.context['form'].errors)

        res = self.client.post(
            (self.update_partner_url),
            payload
        )
        # print(res.context['form'].errors)

        self.assertEqual(res.status_code, 302)
        self.test_partner.refresh_from_db()
        self.assertEqual(self.test_partner.name, payload['name'])
        self.assertRedirects(res, self.partner_dashboard_url)

    def test_delete_partner(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.delete_partner_url)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.partner_dashboard_url)
        self.assertFalse(Partner.objects.filter(id=self.test_partner.id).exists())

    def test_testimonial(self):
        res = self.client.get(self.testimonial_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'testimonial/testimonials.html')

    def test_testimonial_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.testimonial_dashboard_url)
        print(res.context['form'].errors)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'testimonial/testimonial_dashboard.html')

    def test_testimonial_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        photo_file = generate_photo_file()

        res = self.client.post(self.testimonial_dashboard_url, {
            'company': self.test_company.id,
            'name' : 'Test testimonial',
            'content' : 'Testimonial content',
            'company_name' : 'Test Company Name',
            'location' : 'Test Location'
        })
        # print(res.context['form'].errors)
        testimonial = Testimonial.objects.all()[1]

        self.assertEqual(res.status_code, 302)
        self.assertEqual(testimonial.content, 'Testimonial content')
        self.assertRedirects(res, self.testimonial_dashboard_url)

    def test_update_testimonial__GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.update_testimonial_url)
        # print(res.context['form'].errors)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'testimonial/testimonial_dashboard.html')


    def test_update_testimonial_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload =  {
            'company': self.test_company.id,
            'name' : 'Test Client',
            'content' : 'Testimonial content',
            'company_name' : 'Test Company Name',
            'location' : 'Test Location'
        }

        res = self.client.post(
            (self.update_testimonial_url),
            payload
        )
        # print(res.context['form'].errors)

        self.assertEqual(res.status_code, 302)
        self.test_testimonial.refresh_from_db()
        self.assertEqual(self.test_testimonial.name, payload['name'])
        self.assertRedirects(res, self.testimonial_dashboard_url)

    def test_delete_testimonial(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.delete_testimonial_url)
        # print(res.context['form'].errors)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.testimonial_dashboard_url)
        self.assertFalse(Testimonial.objects.filter(id=self.test_testimonial.id).exists())



def tearDownModule():
    paths = {
        'project': os.path.join(settings.MEDIA_ROOT, 'photos/project'),
        'partner': os.path.join(settings.MEDIA_ROOT, 'photos/partner'),
    }

    for label, path in paths.items():
        if os.path.exists(path):
            files = [
                i for i in os.listdir(path)
                if os.path.isfile(os.path.join(path, i)) and i.startswith('test_')
            ]

            for file in files:
                os.remove(os.path.join(path, file))

