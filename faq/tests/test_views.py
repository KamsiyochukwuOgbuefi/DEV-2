import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile

from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse

from faq.models import FAQCategory, FAQQuestion
# from faq.forms import FAQForm

from accounts.models import Account
from company.models import Company  # Import your Company model

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
        self.login_url = reverse('login')
        self.photo_file = generate_photo_file()
        # Create a Account object for testing
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )
        # Create a Company object for testing
        self.test_company = Company.objects.create(
            company_name = 'testcompany',
            website_address = 'http://testcompany.com',
            email = 'test@testcompany.com',
            address_line_1 = 'address line 1',
            city = 'test city',
            state = 'test state',
            postal_code = '111222',
            country = 'test country',
            phone_number = '11122233344',
            user = self.user,
            logo = ContentFile(self.photo_file.read(), 'test_image.png')
        )

        # Create a test category
        self.test_FAQCategory = FAQCategory.objects.create(
            home_note   = 'test home note',
            name = 'test name'
        )

        # Create a FAQ in the test category
        self.test_FAQQuestion = FAQQuestion.objects.create(
            category=self.test_FAQCategory,
            question='Test Question',
            answer='Test Answer',
        )

        self.faq_url = reverse('faq')
        # self.FAQCategory_url = reverse('faq_categories')
        self.FAQQuestion_url = reverse('faq_question', args=[self.test_FAQCategory.id])
        self.faqcategory_dashboard_url = reverse('faqcategory_dashboard')
        self.update_faqcategory_url = reverse('update_faqcategory', args=[self.test_FAQCategory.id])
        self.delete_faqcategory_url = reverse('delete_faqcategory', args=[self.test_FAQCategory.id])
        self.faqquestion_dashboard_url = reverse('faqquestion_dashboard')
        self.update_faqquestion_url = reverse('update_faqquestion', args=[self.test_FAQQuestion.id])
        self.delete_faqquestion_url = reverse('delete_faqquestion', args=[self.test_FAQQuestion.id])
        self.admin_login_url = reverse('admin_login')


    def test_faq_GET(self):
        res = self.client.get(self.faq_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/faq.html')

    def test_faq_question_GET(self):
        res = self.client.get(self.FAQQuestion_url)  # Use the faq_detail_url

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/question.html')

    def test_FAQQuestion_url_GET_invalid_category(self):
        url = reverse('faq_question', args=[999])  # Use an invalid category ID
        res = self.client.get(url)

        self.assertEqual(res.status_code, 404)

    def test_faqcategory_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.faqcategory_dashboard_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/category_dashboard.html')


    def test_faqcategory_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.post(self.faqcategory_dashboard_url, {
            'name': 'test category',
            'home_note': 'test home note'
        })

        self.assertEqual(res.status_code, 302)
        self.assertTrue(FAQCategory.objects.filter(name='test category').exists())
        self.assertRedirects(res, self.faqcategory_dashboard_url)

    def test_update_faqcategory_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })
        res = self.client.get(url_with_args('update_faqcategory', self.test_FAQCategory.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/category_dashboard.html')


    def test_update_faqcategory_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload = {
            'name': 'test category',
            'home_note': 'test home note'
        }

        res = self.client.post(
            url_with_args('update_faqcategory', self.test_FAQCategory.id),
            payload,
        )

        self.assertEqual(res.status_code, 302)
        self.test_FAQCategory.refresh_from_db()
        self.assertEqual(str(self.test_FAQCategory), payload['name'])
        self.assertRedirects(res, self.faqcategory_dashboard_url)
    
    def test_delete_faqcategory(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        test_firm = FAQCategory.objects.create(
            name = 'test category',
            home_note = 'test home note'
        )

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('delete_faqcategory', test_firm.id))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.faqcategory_dashboard_url)
        self.assertFalse(FAQCategory.objects.filter(name='test category').exists())

    def test_faqquestion_dashboard_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(self.faqquestion_dashboard_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/questions_dashboard.html')

    def test_faqquestion_dashboard_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        faqcategory_res = self.client.post(self.faqcategory_dashboard_url, {
            'name': 'test category',
            'home_note': 'test home note'
        })
        faqcategory = FAQCategory.objects.get(name='test category')

        faqquestion_res = self.client.post(self.faqquestion_dashboard_url,{
            'category': faqcategory.id,
            'question': 'test question',
            'answer': 'test asnswer'
        })

        self.assertEqual(faqquestion_res.status_code, 302)
        self.assertTrue(FAQQuestion.objects.filter(category_id=faqcategory.id).exists())
        self.assertRedirects(faqquestion_res, self.faqquestion_dashboard_url)

    def test_delete_faqquetion(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args(
            'delete_faqquestion',
            self.test_FAQQuestion.id
        ))

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.faqquestion_dashboard_url)
        self.assertFalse(
            FAQQuestion.objects.filter(id=self.test_FAQQuestion.id).exists()
        )

    def test_update_faqquestion_GET(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        res = self.client.get(url_with_args('update_faqquestion', self.test_FAQQuestion.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'faq/questions_dashboard.html')

    def test_update_faqquestion_POST(self):
        test_user = Account.objects.get(email='user1@example.com')
        test_user.is_active = True
        test_user.is_admin = True
        test_user.save()

        admin_login_res = self.client.post(self.admin_login_url, {
            'email' : 'user1@example.com',
            'password': 'testpass1234'
        })

        payload = {
            'category': self.test_FAQCategory.id,
            'question': 'test question',
            'answer': 'test asnswer'
        }

        res = self.client.post(
            url_with_args('update_faqquestion', self.test_FAQQuestion.id),
            payload
        )

        self.assertEqual(res.status_code, 302)
        self.test_FAQQuestion.refresh_from_db()
        self.assertRedirects(res, self.faqquestion_dashboard_url)

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

        # Try to access the FAQ category dashboard view as a client
        self.client.login(email='nonadmin@example.com', password='testpass1234')
        res_dashboard = self.client.get(self.faqcategory_dashboard_url)

        # Check that the client is redirected to the login page after attempting to access the FAQ category dashboard
        self.assertEqual(res_dashboard.status_code, 302)
        self.assertFalse(res_dashboard.url.startswith(self.faqcategory_dashboard_url))  # Ensure not redirected to FAQ category dashboard view

        # Try to access the update FAQ category view as a client
        res_update = self.client.get(self.update_faqcategory_url)

        # Check that the client is redirected to the login page when attempting to access the update FAQ category view
        self.assertEqual(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_faqcategory_url))  # Ensure not redirected to update FAQ category view

        # Try to access the delete FAQ category view as a client
        res_delete = self.client.get(self.delete_faqcategory_url)

        # Check that the client is redirected to the login page after attempting to access the delete FAQ category view
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_faqcategory_url))  # Ensure not redirected to delete FAQ category view

        # Try to access the FAQ question dashboard view as a client
        res_faqquestion = self.client.get(self.faqquestion_dashboard_url)

        # Check that the client is redirected to the login page when attempting to access the FAQ question dashboard view
        self.assertEqual(res_faqquestion.status_code, 302)
        self.assertFalse(res_faqquestion.url.startswith(self.faqquestion_dashboard_url))  # Ensure not redirected to FAQ question dashboard view

        # Try to access the update FAQ question view as a client
        res_update = self.client.get(self.update_faqquestion_url)

        # Check that the client is redirected to the login page when attempting to access the update FAQ question view
        self.assertEqual(res_update.status_code, 302)
        self.assertFalse(res_update.url.startswith(self.update_faqquestion_url))  # Ensure not redirected to update FAQ question view

        # Try to access the delete FAQ question view as a client
        res_delete = self.client.get(self.delete_faqquestion_url)

        # Check that the client is redirected to the login page after attempting to access the delete FAQ question view
        self.assertEqual(res_delete.status_code, 302)
        self.assertFalse(res_delete.url.startswith(self.delete_faqquestion_url))  # Ensure not redirected to delete FAQ question view


def tearDownModule():
    images_path = os.path.join(settings.MEDIA_ROOT, 'photos/logos')
    files = [i for i in os.listdir(images_path)
            if os.path.isfile(os.path.join(images_path, i))
            and i.startswith('test_')]

    for file in files:
        os.remove(os.path.join(images_path, file))
