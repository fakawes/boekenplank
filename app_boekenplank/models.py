from distutils.command.upload import upload
from random import choices
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
        
class Category(models.Model):
    name = models.CharField(max_length=40)
    def __str__(self) -> str:
        return self.name

class Category_test(models.Model):
    category = models.ManyToManyField(Category)

class Author(models.Model):
    firstname = models.CharField(max_length=20,default='')
    lastname = models.CharField(max_length=20,default='')
    birthday = models.DateField()
    image = models.ImageField(upload_to='author_images',null=True)
    about = models.TextField(max_length=500,null=True)
    
    def __str__(self) -> str:
        return '{} {}'.format(self.firstname, self.lastname)

class Book(models.Model):
    title = models.CharField(max_length=200,null=True,default='')
    publisher = models.ManyToManyField(Publisher)
    year = models.DateField()
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='book_images')
    
    def __str__(self) -> str:
        return '{} | {}'.format(self.title,self.author)
    
class BookReview(models.Model):
    SCORE_CHOISES = (
        (1,'TERRIBLE'),
        (2,'BAD'),
        (3,'OK'),
        (4,'GOOD'),
        (5,'GREAT'),
        (6,'EXCELLENT'),    
    )
    title = models.CharField(max_length=50,)
    reviewText = models.TextField(max_length=500,null=True)
    score = models.IntegerField(choices=SCORE_CHOISES)
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    def __str__(self) -> str:
        return self.title
