from django.db.models import F
from django.test.utils import CaptureQueriesContext
from django.db import connection
from django.contrib.auth.models import User

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from ..models import Category, Book, BookReaderRelation
from ..serializers import BookSerializer, BookReaderSerializer


class ApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='vlad')
        self.user2 = User.objects.create(username='zxc')
        cat1 = Category.objects.create(title='Book')
        self.book1 = Book.objects.create(title="First book", author_id=self.user.id, pages=100, cat=cat1)
        self.book2 = Book.objects.create(title="Second book", author_id=self.user.id, pages=200, cat=cat1)

        self.rel1 = BookReaderRelation.objects.create(book=self.book1, reader=self.user, pages_read=12, info='QWE', bool=True, mark=3)
        self.rel2 = BookReaderRelation.objects.create(book=self.book1, reader=self.user2, pages_read=50, info='zxc', bool=False, mark=5)

    def test_get(self):
        url = reverse('BookViewSet-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            # print(response)
            # print("queries -----", queries)
            self.assertEqual(1, len(queries))
            # print('queries ===', len(queries))

        books = Book.objects.all().annotate().annotate(author_name=F("author__username"), category=F("cat__title"))

        serializer_data = BookSerializer(books, many=True).data

        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['title'], "First book")
        self.assertEqual(HTTP_200_OK, response.status_code)

    def test_get_BRR(self):
        url = reverse('BookReaderViewSet-list')

        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)

            self.assertEqual(1, len(queries))

        rels = BookReaderRelation.objects.all().annotate(book_title=F('book__title'), reader_name=F('reader__username'),)

        serializer_data = BookReaderSerializer(rels, many=True).data

        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['pages_read'], 12)
        self.assertEqual(HTTP_200_OK, response.status_code)


