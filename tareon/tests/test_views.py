# import os
# import io
# import shutil
# from django.conf import settings
# from django.core.files.base import ContentFile

# from PIL import Image

# from django.test import TestCase, Client
# from django.urls import reverse

# from accounts.models import Account
# from company.models import Company, CompanyOverview
# from service.models import Service, ServiceProcess
# from staff.models import Staff

# from django.utils import timezone
# from datetime import datetime

# from django.conf.urls import handler404, handler500

# def generate_photo_file():
#     file         = io.BytesIO()
#     image        = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
#     image.save(file, 'png')
#     file.name    = 'test_image.png'
#     file.seek(0)
#     return file

# def url_with_args(name, args):
#     return reverse(name, args=[args])

# class TestViews(TestCase):

#     def setUp(self):
#         self.client     = Client()
#         self.home_url   = reverse('home')
#         self.photo_file = generate_photo_file()
#         self.user       = Account.objects.create_user(
#             first_name = 'first',
#             last_name  = 'last',
#             email      = 'user1@example.com',
#             password   = 'testpass1234',
#             username   = 'first_last'
#         )

#         # Create a company
#         self.logo_file   = generate_photo_file()
#         self.test_company = Company.objects.create(
#             id               = 1,
#             company_name     = 'testcompany',
#             website_address  = 'http://testcompany.com',
#             email            = 'test@testcompany.com',
#             address_line_1   = 'address line 1',
#             address_line_2   = 'address line 2',
#             city             = 'test city',
#             state            = 'test state',
#             postal_code      = 'test code',
#             country          = 'test country',
#             phone_number     = '+123456789',
#             logo             = ContentFile(self.logo_file.read(), 'test_logo.png'),
#             is_client        = False,
#             facebook         = 'test_facebook',
#             twitter          = 'test_twitter',
#             linkedin         = 'test_linkedin',
#             instagram        = 'test_instagram',
#             youtube          = 'test_youtube',
#             user             = self.user,
#         )

#         # Create a company overview
#         self.test_company_overview = CompanyOverview.objects.create(
#             company          = self.test_company,
#             purpose          = 'test purpose',
#             mission          = 'test mission statement',
#             vision           = 'test vision',
#             core_values      = 'test core values',
#             ims_policy       = 'test IMS policy',
#         )

#         self.setUp_file   = generate_photo_file()
#         # Create a service
#         self.test_service = Service.objects.create(
#             company     = self.test_company,
#             name        = 'test service',
#             slug        = 'test_service',
#             description = 'my test service',
#             image       = ContentFile(self.setUp_file.read(), 'test_image.png')
#         )

#         # Create a service process
#         self.test_service_process = ServiceProcess.objects.create(
#             company     = self.test_company,
#             service     = self.test_service,
#             name        = 'test process',
#             description = 'my test process',
#             image       = ContentFile(self.setUp_file.read(), 'test_image.png')
#         )

#         # Create a staff
#         self.test_staff = Staff.objects.create(
#             company      = self.test_company,
#             first_name   = 'test first',
#             last_name    = 'test last',
#             position     = 'test job',
#             image        = ContentFile(self.setUp_file.read(), 'test_image.png'),
#             description  = 'my test description'
#         )

#     def test_home(self):
#         res = self.client.get(self.home_url)

#         self.assertEqual(res.status_code, 200)
#         self.assertTemplateUsed(res, 'home.html')

    # def test_error_500(self):
    #     self.client.raise_request_exception = False
    #     res = self.client.get(reverse(handler500))
    #     print(handler500.__dir__())
    #     self.assertEqual(res.status_code, 500)
    #     self.assertTrue('Sorry the Page Could not be Found' in res.content.decode('utf8'))



# Cleans up test-generated image files from specified directories after tests are run.
# def tearDownModule():
#     # Path to the images of services, service processes, logos, and staff
#     images_paths = {
#         'services'        : os.path.join(settings.MEDIA_ROOT, 'photos/services'),
#         'service_process' : os.path.join(settings.MEDIA_ROOT, 'photos/service_process'),
#         'logos'           : os.path.join(settings.MEDIA_ROOT, 'photos/logos'),
#         'staff'           : os.path.join(settings.MEDIA_ROOT, 'photos/staffs')  # Add staff images directory
#     }

#     # Iterate over all the paths
#     for key, path in images_paths.items():
#         files = [
#             i for i in os.listdir(path)
#             if os.path.isfile(os.path.join(path, i)) and i.startswith('test_')
#         ]

#         for file in files:
#             os.remove(os.path.join(path, file))
