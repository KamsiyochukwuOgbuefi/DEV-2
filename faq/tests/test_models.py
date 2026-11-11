from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from faq.models import FAQCategory, FAQQuestion

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

class TestFAQModels(TestCase):

    def test_create_faq_category(self):
        home_note = 'test home note'
        name = 'test name'
        category = create_FAQCategory()

        self.assertEqual(str(category), name)
        self.assertEqual(category.home_note, home_note)

    def test_create_FAQQuestion(self):
        category = create_FAQCategory()
        question = 'test question'
        answer = 'test answer'

        faq = create_FAQQuestion(category)

        self.assertEqual(str(faq), question)
        self.assertEqual(faq.category, category)
        self.assertEqual(faq.answer, answer)
