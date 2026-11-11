from django.test import TestCase
from django.urls import reverse, resolve
from faq.views import ( 
    faq, faq_question,faqcategory_dashboard, update_faqcategory, delete_faqcategory, 
    faqquestion_dashboard, update_faqquestion, delete_faqquestion
)
from faq.models import FAQCategory, FAQQuestion
from company.models import Company, CompanyOverview
from accounts.models import Account

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

def url_with_args(name, args):
    return reverse(name, args=[args])

def create_FAQCategory(
    home_note   = 'test home note',
    name = 'test name'
):
    return FAQCategory.objects.create(
        home_note = home_note,
        name = name
    )

def create_FAQQuestion(
    category,
    question = 'test question',
    answer = 'test answer'
):
    return FAQQuestion.objects.create(
        category = category,
        question = question,
        answer = answer
    )


class TestUrls(TestCase):

    def test_faq_url_resolves(self):
        url = reverse('faq')
        self.assertEqual(resolve(url).func, faq)

    def test_faq_detail_url_resolves(self):
        category = create_FAQCategory()
        url = url_with_args('faq_question', category.id)
        self.assertEqual(resolve(url).func, faq_question)

    def test_faqcategory_dashboard_url_resolves(self):
        url = reverse('faqcategory_dashboard')
        self.assertEqual(resolve(url).func, faqcategory_dashboard)

    def test_update_faqcategory_url_resolves(self):
        category = create_FAQCategory()
        url = url_with_args('update_faqcategory', category.id)
        self.assertEqual(resolve(url).func, update_faqcategory)

    def test_delete_faqcategory_urls_resolves(self):
        category = create_FAQCategory()
        url = url_with_args('delete_faqcategory', category.id)
        self.assertEqual(resolve(url).func, delete_faqcategory)

    def test_faqquestion_dashboard_url_resolves(self):
        url = reverse('faqquestion_dashboard')
        self.assertEqual(resolve(url).func, faqquestion_dashboard)

    def test_update_faqquestion_url_resolves(self):
        category = create_FAQCategory()
        question = create_FAQQuestion(category)
        url = url_with_args('update_faqquestion', question.id)
        self.assertEqual(resolve(url).func, update_faqquestion)

    def test_delete_faqquestion_urls_resolves(self):
        category = create_FAQCategory()
        question = create_FAQQuestion(category)
        url = url_with_args('delete_faqquestion', question.id)
        self.assertEqual(resolve(url).func, delete_faqquestion)