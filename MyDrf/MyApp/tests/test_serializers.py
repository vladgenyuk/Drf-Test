from django.contrib.auth.models import User
from django.db.models import F
from django.test import TestCase

from ..models import Category, Book, BookReaderRelation
from ..serializers import BookSerializer, BookReaderSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='vlad')
        self.user2 = User.objects.create(username='arsen')


    def test_ok(self):
        cat1 = Category.objects.create(title='Book')
        book1 = Book.objects.create(title="First book", author_id=self.user.id, pages=100, cat=cat1)
        book2 = Book.objects.create(title="Second book", author_id=self.user.id, pages=200, cat=cat1)
        rel1 = BookReaderRelation.objects.create(book=book1, reader=self.user, pages_read=12, info='QWE', bool=True, mark=3)
        rel2 = BookReaderRelation.objects.create(book=book1, reader=self.user2, pages_read=50, info='zxc', bool=False, mark=5)

        books = Book.objects.all().annotate(author_name=F("author__username"), category=F("cat__title"))
        rels = BookReaderRelation.objects.all().annotate(book_title=F('book__title'), reader_name=F('reader__username'),)
        data = BookSerializer(books, many=True).data
        data2 = BookReaderSerializer(rels, many=True).data
        #print(data2)
        expected_data = [
                {
                    "id": 1,
                    "title": "First book",
                    "pages": 100,
                    "category": "Book",
                    "author_name": "vlad"
                },
                {
                    "id": 2,
                    "title": "Second book",
                    "pages": 200,
                    "category": "Book",
                    "author_name": "vlad"
                },
            ]
        expected_data2 = [
                {
                "id": 1,
                "book_title": "First book",
                "reader_name": "vlad",
                "pages_read": 12,
                "info": "QWE",
                "bool": True,
                "mark": 3
            },
            {
                "id": 2,
                "book_title": "First book",
                "reader_name": "arsen",
                "pages_read": 50,
                "info": "zxc",
                "bool": False,
                "mark": 5
            },
        ]
        self.assertEqual(expected_data, data)
        self.assertEqual(expected_data2, data2)
