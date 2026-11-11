import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Account
from company.models import Company
from service.models import Service, ServiceProcess

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test_image.png'
    file.seek(0)
    return file

def url_with_args(name, args):
    return reverse(name, args=[args])


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.service_dashboard_url = reverse('service_dashboard')
        self.SPD_url = reverse('service_process_dashboard')
        self.company_dashboard_url = reverse('company_dashboard')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.admin_login_url = reverse('admin_login')
        self.setUp_file = generate_photo_file()

        self.user = Account.objects.create_user(
            first_name    = 'first',
            last_name     = 'last',
            email         = 'user1@example.com',
            password      = 'testpass1234',
            username      = 'first_last'
        )
        self.user2 = Account.objects.create_user(
            first_name    = 'first2',
            last_name     = 'last2',
            email         = 'user2@example.com',
            password      = 'testpass5678',
            username      = 'first2_last2'
        )
        self.test_company   = Company.objects.create(
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
            user            = self.user,
            logo            = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        self.test_service = Service.objects.create(
            company             = self.test_company,
            name                = 'test service',
            slug                = 'test_service',
            description         =  'my test service',
            image               = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        self.test_service_process = ServiceProcess.objects.create(
            company               = self.test_company,
            service               = self.test_service,
            name                  = 'test process',
            description           = 'my test process',
            image                 = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        
        self.update_service_url = reverse('update_service', args=[self.test_service.id])
        self.delete_service_url = reverse('delete_service', args=[self.test_service.id])
        self.update_service_process_url = reverse('update_service_process', args=[self.test_service_process.id])
        self.delete_service_process_url = reverse('delete_service_process', args=[self.test_service_process.id])


    def test_service(self):
        res = self.client.get(url_with_args('service_slug',  self.test_service.slug))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service.html')


    def test_service_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.service_dashboard_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_dashboard.html')

    def test_service_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        res = self.client.post(self.service_dashboard_url, {
            'company'               : self.test_company.id,
            'name'                  : 'test service two',
            'slug'                  : 'test_service_two',
            'description'           : 'my test service',
            'image'                 : photo_file,
        }, format='multipart')

        # Debugging form errors
        # print(res.context['form'].errors)  # Check what errors are being returned

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Company.objects.filter(email='test@testcompany.com').exists())
        self.assertTrue(Service.objects.filter(name='test service two').exists())

        self.assertRedirects(res, self.service_dashboard_url)

    def test_update_service_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_service', self.test_service.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_dashboard.html')

    def test_update_service_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload = {
            'company'               : self.test_company.id,
            'name'                  : 'updated  service',
            'slug'                  : 'updated_service',
            'description'           : 'updated  service description',
            'image'                 : photo_file
        }

        res = self.client.post(
            url_with_args('update_service', self.test_service.id),
            payload,
            format='multipart'
        )

        # Debugging form errors
        # print(res.context['form'].errors)  # Check what errors are being returned

        self.assertEqual(res.status_code, 302)
        self.test_service.refresh_from_db()
        self.assertEqual(str(self.test_service), payload['name'])
        self.assertRedirects(res, self.service_dashboard_url)

    def test_delete_service(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        test_service = Service.objects.create(
            company             = self.test_company,
            name                = 'test service three',
            slug                = 'test_service_three',
            description         =  'my test service'
        )

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })


        res = self.client.get(url_with_args('delete_service', test_service.id))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.service_dashboard_url)
        self.assertFalse(Company.objects.filter(email='test@testcompany2.com').exists())

    def test_SPD_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.SPD_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_process_dashboard.html')

    def test_SPD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        SPD_res = self.client.post(self.SPD_url, {
            'company'               : self.test_company.id,
            'service'               : self.test_service.id,
            'name'                  : 'test process',
            'description'           : 'my test process',
            'image'                 : photo_file,
        }, format='multipart')
        # test_sdp = ServiceProcess.objects.all()[1]
        # print(test_sdp.id)

        self.assertEqual(SPD_res.status_code, 302)
        self.assertTrue(Service.objects.filter(company_id=self.test_company.id).exists())
        self.assertTrue(ServiceProcess.objects.filter(service_id=self.test_service.id).exists())
        self.assertRedirects(SPD_res, self.SPD_url)

    def test_update_service_process_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_service_process', self.test_service_process.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'service/service_process_dashboard.html')

    def test_update_service_process_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        payload ={
            'company'               :  self.test_company.id,
            'service'               :  self.test_service.id,
            'name'                  : 'test process',
            'description'           : 'my test process',
            'image'                 :  photo_file,
        }

        res = self.client.post(
            url_with_args('update_service_process', self.test_service_process.id),
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 302)
        self.test_service_process.refresh_from_db()
        self.assertRedirects(res, self.SPD_url)

    def test_delete_service_process(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        process = ServiceProcess.objects.all()[0]

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        # print(process.id)

        res = self.client.get(url_with_args(
            'delete_service_process',
            self.test_service_process.id
        ))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.SPD_url)
        self.assertFalse(
            ServiceProcess.objects.filter(id=self.test_service_process.id).exists()
        )

    def test_non_admin_user_access(self):
        # Create a client user
        self.user = Account.objects.create_user(
            first_name='first',
            last_name='last',
            email='nonadmin@example.com',
            password='testpass1234',
            username='test first_last'
        )

        # Make the client user as a client, not an admin
        self.user.is_admin = False  # Set 'is_admin' to False to make the user a client
        self.user.is_active = True  # Set 'is_active' to True
        self.user.save()

        # Try to access the service dashboard view as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        res_dashboard = self.client.get(self.service_dashboard_url)

        # Check that the client is redirected to the login page after attempting to access the service dashboard
        self.assertEqual(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.service_dashboard_url))  # Ensure not redirected to service dashboard view

        # Try to access the update service view as a client
        res_update = self.client.get(self.update_service_url)

        # Check that the client is redirected to the login page when attempting to access the update service view
        self.assertEqual(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_service_url))  # Ensure not redirected to update service view

        # Try to access the delete service view as a client
        res_delete = self.client.get(self.delete_service_url)

        # Check that the client is redirected to the login page after attempting to access the delete service view
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_service_url))  # Ensure not redirected to delete service view

        # Try to access the SPD view as a client
        res_spd = self.client.get(self.SPD_url)

        # Check that the client is redirected to the login page when attempting to access the SPD view
        self.assertEqual(res_spd.status_code, 302)
        self.assertFalse(res_spd.url.startswith(self.SPD_url))  # Ensure not redirected to SPD view

        # Try to access the update service process view as a client
        res_update = self.client.get(self.update_service_process_url)

        # Check that the client is redirected to the login page when attempting to access the update service process view
        self.assertEqual(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_service_process_url))  # Ensure not redirected to update service process view

        # Try to access the delete service process view as a client
        res_delete = self.client.get(self.delete_service_process_url)

        # Check that the client is redirected to the login page after attempting to access the delete service process view
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_service_process_url))  # Ensure not redirected to delete service process view

 
def tearDownModule():
    paths = {
        'services': os.path.join(settings.MEDIA_ROOT, 'photos/services'),
        'service_process': os.path.join(settings.MEDIA_ROOT, 'photos/service_process'),
        'logos': os.path.join(settings.MEDIA_ROOT, 'photos/logos'),
    }

    for label, path in paths.items():
        if os.path.exists(path):
            files = [
                i for i in os.listdir(path)
                if os.path.isfile(os.path.join(path, i)) and i.startswith('test_')
            ]

            for file in files:
                os.remove(os.path.join(path, file))

