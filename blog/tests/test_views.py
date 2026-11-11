import os
import io
import shutil
from django.conf import settings
from django.core.files.base import ContentFile


from PIL import Image

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models import Account
from company.models import Company, CompanyOverview
from blog.models import Article, Paragraph

def generate_photo_file():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    # file.name = 'test_image.png'
    file.seek(0)
    return file


def url_with_args(name, args):
    return reverse(name, args=[args])

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.blog_url = reverse('blog')
        self.search_url = reverse('search')
        self.photo_file = generate_photo_file()
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
            user = self.user,
            logo = ContentFile(self.photo_file.read(), 'test_image.png'),
        )

        self.article = Article.objects.create(
            article_title = 'Test Title',
            article_subtitle = 'Test Subtitle',
            image = ContentFile(self.photo_file.read(), 'test_image.png'),
            tags = 'testing, test, tagging, tags'
        )
        self.paragraph = Paragraph.objects.create(
            article = self.article,
            paragraph_title = 'paragraph title',
            paragraph_content = 'test paragraph content'
        )


    def test_article(self):
        res = self.client.get(url_with_args('article', self.article.id))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'blog/article.html')

    def test_blog(self):
        res = self.client.get(self.blog_url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'blog/blog.html')

    def test_blog_by_keyword(self):
        res = self.client.get(url_with_args('blog_by_keyword', 'test'))

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'blog/blog.html')

    def test_search(self):
        res = self.client.get(self.search_url)

        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, self.blog_url)

    def test_search_with_keyword(self):
        res = self.client.get(self.search_url + '?keyword=test')

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'blog/blog.html')



def tearDownModule():
    paths = {
        'article': os.path.join(settings.MEDIA_ROOT, 'photos/article'),
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
