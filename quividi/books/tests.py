from .models import Book, Notation, Author
from django.contrib.auth.models import User
import pytest
from django.test import RequestFactory
from django.test import Client
from datetime import datetime
# Create your tests here.


@pytest.mark.django_db
def test_new_notation():

    # create user
    user = User.objects.create_user('test', 'email@test.com', 'password')
    # create author
    author = Author.objects.create(name="author_1")
    # create book
    book = Book.objects.create(title="title", author=author, summary="blablabla", year=2019)
    # create succesfully first notation
    firt_notation = Notation.objects.create(user_author=user, book=book, note=3, description="blabla")
    
    
    #Connect to website and create second notation (should failed)
    client = Client()
    assert(client.login(username='test', password='password') == True)

    response = client.post('/books/book/1', {
        'user_author': 1,
        'book': 1,
        'date': '2019-12-05',
        'initial-date': '2019-12-05 09:42:28',
        'note': 3,
        'description': "plop"
        })

    assert(response.status_code == 401)

