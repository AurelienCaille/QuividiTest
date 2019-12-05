from django.db import models
import datetime
import django
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):

    title = models.CharField(max_length=50)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000)
    year = models.IntegerField(default=datetime.datetime.now().year)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class Author(models.Model):

    name = models.CharField(max_length=50)


    def __str__(self):
        return self.name


class Notation(models.Model):

    user_author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now)
    note = models.IntegerField(
        default=3,
        validators=[MaxValueValidator(5), MinValueValidator(0)]
    )
    description = models.TextField(max_length=300, default="")
    
    
    def __str__(self):
        return str(self.book) + ':' + str(self.note)