from django import forms
from dataclasses import field
from unicodedata import category
from django.forms import CheckboxSelectMultiple, ModelForm
from app_boekenplank.models import Book, BookReview, Author, Publisher, Category, Category_test

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title','publisher','year','author','category','image']
        
        widgets = {
            'category': forms.CheckboxSelectMultiple() 
        }
        


class CategoryForm(ModelForm):
    class Meta:
        model = Category_test
        fields = ['category']
          
class ReviewForm(ModelForm):
    class Meta:
        model = BookReview
        fields = ['title','reviewText','score','book']


class AuthorForm(ModelForm):
    class Meta: 
        model = Author
        fields = ['firstname', 'lastname','birthday','image']
class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']