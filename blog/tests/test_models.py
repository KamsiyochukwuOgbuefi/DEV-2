from django.test import TestCase

from blog.models import Author, Article, Paragraph


def create_author(
    first_name = 'John',
    last_name = 'Doe',
    job_title = 'tester',
    company_name = 'test company',
    email = 'test@test.com',
    phone_number = '111222333'
):
    return Author.objects.create(
        first_name = first_name,
        last_name = last_name,
        job_title = job_title,
        company_name = company_name,
        email = email,
        phone_number = phone_number
    )

def create_article(
    article_title = 'Test Title',
    article_subtitle = 'Test Subtitle'
):
    return Article.objects.create(
        article_title = article_title,
        article_subtitle = article_subtitle
    )

def create_paragraph(
    article,
    paragraph_title = 'paragraph title',
    paragraph_content = 'test paragraph content'
):
    return Paragraph.objects.create(
        article = article,
        paragraph_title = paragraph_title,
        paragraph_content = paragraph_content
    )


class TestModels(TestCase):

    def test_create_author(self):
        first_name = 'John'
        email = 'test@test.com'
        author = create_author()

        self.assertEqual(str(author), first_name)
        self.assertEqual(author.email, email)

    def test_create_article(self):
        article_title = 'Test Title'
        article_subtitle = 'Test Subtitle'
        author = create_author()
        article = create_article()
        article.article_author.add(author)

        self.assertEqual(str(article), article_title)
        self.assertEqual(article.article_subtitle, article_subtitle)
        self.assertIn(author, article.article_author.all())

    def test_create_paragraph(self):
        paragraph_title = 'paragraph title'
        paragraph_content = 'test paragraph content'
        article = create_article()
        paragraph = create_paragraph(article)

        self.assertEqual(str(paragraph), paragraph_title)
        self.assertEqual(paragraph.paragraph_content, paragraph_content)



