from django.test import TestCase
from django.urls import reverse, resolve
from project.views import (
   service_projects, project, project_dashboard, update_project,
   delete_project, partner_dashboard, update_partner, delete_partner,
   testimonial, testimonial_dashboard, update_testimonial, delete_testimonial
)
import datetime
from django.utils import timezone

from accounts.models import Account
from company.models import Company
from service.models import Service
from project.models import (
    Project, ProjectImages, Partner, Testimonial
)

def url_with_args(name, args):
    return reverse(name, args=[args])

class TestUrls(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name  = 'last',
            email      = 'user1@example.com',
            password   = 'testpass1234',
            username   = 'first_last'
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
            company     = self.test_company,
            name        = 'Testing Service',
            slug        = 'testing_service',
            description = 'Testing service description'
        )
        self.test_project = Project.objects.create(
            company         = self.test_company,
            service         = self.test_service,
            title           = 'Test Project Title',
            project_scope   = 'Test Project Scope',
            project_url     = 'http://projecturl.com',
            completion_date = timezone.make_aware(datetime.datetime(2025, 1, 1))
        )
        self.test_image = ProjectImages.objects.create(
            company     = self.test_company,
            service     = self.test_service,
            project     = self.test_project,
            name        = 'Test Image',
            description = 'Test Image Description'
        )
        self.test_partner = Partner.objects.create(
            company = self.test_company,
            name    = 'Test Partner',
        )
        self.test_testimonial = Testimonial.objects.create(
            company      = self.test_company,
            name         = 'Test Client',
            content      = 'Testimonial content',
            company_name = 'Test Company Name',
            location     = 'Test Location'
        )

    def test_service_projects_urls_resolves(self):
        url = url_with_args('service_projects', self.test_service.slug)
        self.assertEqual(resolve(url).func, service_projects)

    def test_project_urls_resolves(self):
        url = url_with_args('project', self.test_project.id)
        self.assertEqual(resolve(url).func, project)

    def test_project_dashboard_urls_resolves(self):
        url = reverse('project_dashboard')
        self.assertEqual(resolve(url).func, project_dashboard)

    def test_update_project_urls_resolves(self):
        url = url_with_args('update_project', self.test_project.id)
        self.assertEqual(resolve(url).func, update_project)

    def test_delete_project_urls_resolves(self):
        url = url_with_args('delete_project', self.test_project.id)
        self.assertEqual(resolve(url).func, delete_project)

    def test_partner_dashboard_urls_resolves(self):
        url = reverse('partner_dashboard')
        self.assertEqual(resolve(url).func, partner_dashboard)

    def test_update_partner_urls_resolves(self):
        url = url_with_args('update_partner', self.test_partner.id)
        self.assertEqual(resolve(url).func, update_partner)

    def test_delete_partner_urls_resolves(self):
        url = url_with_args('delete_partner', self.test_partner.id)
        self.assertEqual(resolve(url).func, delete_partner)

    def test_testimonial_urls_resolves(self):
        url = reverse('testimonial')
        self.assertEqual(resolve(url).func, testimonial)

    def test_testimonial_dashboard_urls_resolves(self):
        url = reverse('testimonial_dashboard')
        self.assertEqual(resolve(url).func, testimonial_dashboard)

    def test_update_testimonial_urls_resolves(self):
        url = url_with_args('update_testimonial', self.test_testimonial.id)
        self.assertEqual(resolve(url).func, update_testimonial)

    def test_delete_testimonial_urls_resolves(self):
        url = url_with_args('delete_testimonial', self.test_testimonial.id)
        self.assertEqual(resolve(url).func, delete_testimonial)
