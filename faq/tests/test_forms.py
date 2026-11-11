from django.test import TestCase
from faq.forms import FAQCategoryForm, FAQQuestionForm
from accounts.models import Account
from company.models import Company, CompanyOverview
from faq.models import FAQCategory, FAQQuestion


class TestForms(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(
            first_name = 'first',
            last_name = 'last',
            email = 'user1@example.com',
            password = 'testpass1234',
            username = 'first_last'
        )
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
            user = self.user
        )
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

    def test_faq_category_form_valid_data(self):

        data = {
            'name': 'test category',
            'home_note': 'test home note'
        }

        form = FAQCategoryForm(data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_faq_category_form_no_data(self):
        form = FAQCategoryForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_faq_question_form_valid_data(self):

        data = {
            'category': self.test_FAQCategory.id,
            'question': 'test question',
            'answer': 'test answer'
        }

        form = FAQQuestionForm(data)

        self.assertTrue(form.is_valid())
        self.assertFalse(form.errors)

    def test_faqquestion_form_no_data(self):
        form = FAQQuestionForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
