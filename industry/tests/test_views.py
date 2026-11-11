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
from industry.models import Industry, IndustryProcess

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
        self.industry_dashboard_url = reverse('industry_dashboard')
        self.IPD_url = reverse('industry_process_dashboard')
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
        self.test_industry = Industry.objects.create(
            company             = self.test_company,
            name                = 'test industry',
            slug                = 'test_industry',
            description         =  'my test industry',
            image               = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        self.test_industry_process = IndustryProcess.objects.create(
            company               = self.test_company,
            industry               = self.test_industry,
            name                  = 'test process',
            description           = 'my test process',
            image                 = ContentFile(self.setUp_file.read(), 'test_image.png')
        )
        
        self.update_industry_url = reverse('update_industry', args=[self.test_industry.id])
        self.delete_industry_url = reverse('delete_industry', args=[self.test_industry.id])
        self.update_industry_process_url = reverse('update_industry_process', args=[self.test_industry_process.id])
        self.delete_industry_process_url = reverse('delete_industry_process', args=[self.test_industry_process.id])


    def test_industry(self):
        res = self.client.get(url_with_args('industry_slug',  self.test_industry.slug))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'industry/industry.html')


    def test_industry_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.industry_dashboard_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'industry/industry_dashboard.html')

    def test_industry_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        res = self.client.post(self.industry_dashboard_url, {
            'company'               : self.test_company.id,
            'name'                  : 'test industry two',
            'slug'                  : 'test_industry_two',
            'description'           : 'my test industry',
            'image'                 : photo_file,
        }, format='multipart')

        # Debugging form errors
        # print(res.context['form'].errors)  # Check what errors are being returned

        self.assertEqual(res.status_code, 302)
        self.assertTrue(Company.objects.filter(email='test@testcompany.com').exists())
        self.assertTrue(Industry.objects.filter(name='test industry two').exists())

        self.assertRedirects(res, self.industry_dashboard_url)

    def test_update_industry_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_industry', self.test_industry.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'industry/industry_dashboard.html')

    def test_update_industry_POST(self):
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
            'name'                  : 'updated  industry',
            'slug'                  : 'updated_industry',
            'description'           : 'updated  industry description',
            'image'                 : photo_file
        }

        res = self.client.post(
            url_with_args('update_industry', self.test_industry.id),
            payload,
            format='multipart'
        )

        # Debugging form errors
        # print(res.context['form'].errors)  # Check what errors are being returned

        self.assertEqual(res.status_code, 302)
        self.test_industry.refresh_from_db()
        self.assertEqual(str(self.test_industry), payload['name'])
        self.assertRedirects(res, self.industry_dashboard_url)

    def test_delete_industry(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        test_industry = Industry.objects.create(
            company             = self.test_company,
            name                = 'test industry three',
            slug                = 'test_industry_three',
            description         =  'my test industry'
        )

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })


        res = self.client.get(url_with_args('delete_industry', test_industry.id))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.industry_dashboard_url)
        self.assertFalse(Company.objects.filter(email='test@testcompany2.com').exists())

    def test_IPD_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.IPD_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'industry/industry_process_dashboard.html')

    def test_IPD_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        photo_file = generate_photo_file()

        IPD_res = self.client.post(self.IPD_url, {
            'company'               : self.test_company.id,
            'industry'               : self.test_industry.id,
            'name'                  : 'test process',
            'description'           : 'my test process',
            'image'                 : photo_file,
        }, format='multipart')
        # test_sdp = industryProcess.objects.all()[1]
        # print(test_idp.id)

        self.assertEqual(IPD_res.status_code, 302)
        self.assertTrue(Industry.objects.filter(company_id=self.test_company.id).exists())
        self.assertTrue(IndustryProcess.objects.filter(industry_id=self.test_industry.id).exists())
        self.assertRedirects(IPD_res, self.IPD_url)

    def test_update_industry_process_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        # print(self.test_industry_process.id)
        res = self.client.get(url_with_args('update_industry_process', self.test_industry_process.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'industry/industry_process_dashboard.html')

    def test_update_industry_process_POST(self):
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
            'industry'              :  self.test_industry.id,
            'name'                  : 'test process',
            'description'           : 'my test process',
            'image'                 :  photo_file,
        }

        res = self.client.post(
            url_with_args('update_industry_process', self.test_industry_process.id),
            payload,
            format='multipart'
        )

        self.assertEqual(res.status_code, 302)
        self.test_industry_process.refresh_from_db()
        self.assertRedirects(res, self.IPD_url)

    def test_delete_industry_process(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        process = IndustryProcess.objects.all()[0]

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        # print(process.id)

        res = self.client.get(url_with_args(
            'delete_industry_process',
            self.test_industry_process.id
        ))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.IPD_url)
        self.assertFalse(
            IndustryProcess.objects.filter(id=self.test_industry_process.id).exists()
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

        # Try to access the industry dashboard view as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        res_dashboard = self.client.get(self.industry_dashboard_url)

        # Check that the client is redirected to the login page after attempting to access the industry dashboard
        self.assertEqual(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.industry_dashboard_url))  # Ensure not redirected to industry dashboard view

        # Try to access the update industry view as a client
        res_update = self.client.get(self.update_industry_url)

        # Check that the client is redirected to the login page when attempting to access the update industry view
        self.assertEqual(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_industry_url))  # Ensure not redirected to update industry view

        # Try to access the delete industry view as a client
        res_delete = self.client.get(self.delete_industry_url)

        # Check that the client is redirected to the login page after attempting to access the delete industry view
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_industry_url))  # Ensure not redirected to delete industry view

        # Try to access the ipd view as a client
        res_ipd = self.client.get(self.IPD_url)

        # Check that the client is redirected to the login page when attempting to access the ipd view
        self.assertEqual(res_ipd.status_code, 302)
        self.assertFalse(res_ipd.url.startswith(self.IPD_url))  # Ensure not redirected to ipd view

        # Try to access the update industry process view as a client
        res_update = self.client.get(self.update_industry_process_url)

        # Check that the client is redirected to the login page when attempting to access the update industry process view
        self.assertEqual(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_industry_process_url))  # Ensure not redirected to update industry process view

        # Try to access the delete industry process view as a client
        res_delete = self.client.get(self.delete_industry_process_url)

        # Check that the client is redirected to the login page after attempting to access the delete industry process view
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_industry_process_url))  # Ensure not redirected to delete industry process view

 
def tearDownModule():
    paths = {
        'industries': os.path.join(settings.MEDIA_ROOT, 'photos/industries'),
        'industry_process': os.path.join(settings.MEDIA_ROOT, 'photos/industry_process'),
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

