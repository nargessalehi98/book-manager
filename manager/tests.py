from datetime import date
from decimal import Decimal
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Book
from .serializer import BookSerializer
from rest_framework.test import APITestCase


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book(
            title='The Great Gatsby',
            author='F. Scott Fitzgerald',
            publication_date=date(1925, 4, 10),
            price=Decimal('9.99'),
            cover_image_url='https://example.com/great-gatsby-cover.jpg',
            description='A classic novel about the Jazz Age.',
            num_pages=180,
            subjects='fiction,literature',
            updated=False
        )

    def test_book_is_updated(self):
        self.assertFalse(self.book.is_updated())
        self.book.update_extra_info(num_pages=200, subjects=['fiction', 'classic'], description='An American Classic',
                                    cover_imager_url='https://example.com/great-gatsby-new-cover.jpg')
        self.assertTrue(self.book.is_updated())

    def test_set_subject_list(self):
        self.book.set_subject_list(['fiction', 'literature'])
        self.assertEqual(self.book.subjects, 'fiction,literature')

    def test_get_subject_list(self):
        self.book.set_subject_list(['fiction', 'classic'])
        self.assertEqual(self.book.get_subject_list(), ['fiction', 'classic'])

    def test_create_title_query(self):
        self.assertEqual(self.book.create_title_query(), 'The+Great+Gatsby')

    def test_update_extra_info(self):
        self.book.update_extra_info(num_pages=200, subjects=['fiction', 'classic'], description='An American Classic',
                                    cover_imager_url='https://example.com/great-gatsby-new-cover.jpg')
        self.assertEqual(self.book.num_pages, 200)
        self.assertEqual(self.book.get_subject_list(), ['fiction', 'classic'])
        self.assertEqual(self.book.description, 'An American Classic')
        self.assertEqual(self.book.cover_image_url, 'https://example.com/great-gatsby-new-cover.jpg')
        self.assertTrue(self.book.updated)


class BookListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_book_list(self):
        book1 = Book.objects.create(title='Book 1', author='Author 1', updated=True, publication_date='2020-12-12',
                                    price=12)
        book2 = Book.objects.create(title='Book 2', author='Author 2', updated=True, publication_date='2020-12-12',
                                    price=12)
        book3 = Book.objects.create(title='Book 3', author='Author 3', updated=True, publication_date='2020-12-12',
                                    price=12)

        response = self.client.get('/manager/books/?limit=3&offset=0')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data['results'], list)

        serialized_data = BookSerializer([book1, book2, book3], many=True).data
        self.assertEqual(response.data['results'], serialized_data)


class BookSearchAPIViewTestCase(APITestCase):
    def setUp(self):
        self.book1 = Book.objects.create(title='Test Book 1', author='Test Author', publication_date='2022-01-01',
                                         subjects='test', price=10.00)
        self.book2 = Book.objects.create(title='Test Book 2', author='Test Author', publication_date='2022-02-01',
                                         subjects='test,subject', price=10.00)
        self.book3 = Book.objects.create(title='Another Test Book', author='Another Author',
                                         publication_date='2022-04-01',
                                         subjects='test,subject', price=20.00)

    # How do you think we can make this part cleaner?
    def test_search_by_title(self):
        response = self.client.get('/manager/search/?title=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[1]['title'], 'Test Book 2')

    def test_search_by_author(self):
        response = self.client.get('/manager/search/?author=Test')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[1]['title'], 'Test Book 2')

    def test_search_by_pub_date_range(self):
        response = self.client.get('/manager/search/?pub_date=2022-01-01_2022-03-02')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')
        self.assertEqual(response.data[1]['title'], 'Test Book 2')

    def test_search_by_exact_pub_date(self):
        response = self.client.get('/manager/search/?pub_date=2022-04-01')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Another Test Book')

    def test_search_by_price_exact(self):
        response = self.client.get('/manager/search/?price=10.00')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Book 1')

    def test_search_by_price_range(self):
        response = self.client.get('/manager/search/?price=5.00-15.00')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['title'], 'Test Book 2')

    def test_search_by_subjects(self):
        response = self.client.get('/manager/search/?subjects=test,subject')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Test Book 2')
        self.assertEqual(response.data[1]['title'], 'Another Test Book')
