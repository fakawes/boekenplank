from cProfile import label
# from sqlite3.dbapi2 import _WindowAggregateClass
from django import forms
from dataclasses import field
from unicodedata import category
from django.forms import CheckboxSelectMultiple, EmailField, ModelForm, Textarea
from app_boekenplank.models import Book, BookReview, Author, Publisher, Category, Category_test, DateTest
from django.contrib.auth.models import User
from .widgets import DatePickerInputWidget

from bootstrap_datepicker_plus.widgets import DatePickerInput

class newsLetterForm(forms.Form):
    email = forms.EmailField(label='Email')
    
class contactForm(forms.Form):
    your_name = forms.CharField(label='Your name')
    email = forms.EmailField(label='Email')
    message = forms.CharField(widget=forms.Textarea)
    # message = forms.Text(label='message')

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title','publisher','year','author','category','description','image']
        
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
            'year': DatePickerInputWidget(),
        }
        
class CategoryForm(ModelForm):
    class Meta:
        model = Category_test
        fields = ['category']
          
class ReviewForm(ModelForm):
    class Meta:
        model = BookReview
        fields = ['title','reviewText','score','book']

class DateInput(forms.DateInput):
    input_type = 'date'
class AuthorForm(ModelForm):
    
    
    class Meta: 
        model = Author
        fields = ['firstname', 'lastname','birthday','image']

        widgets = {
            'birthday': DatePickerInput()
        }

class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['name']

class editAccountForm(ModelForm):
    username = forms.CharField(label='Username: ')
    email = forms.EmailField(label='Email: ')
    class Meta:
        model = User
        fields = ['username','email']

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )
class DateForm(ModelForm):
    
    
    class Meta: 
        model = DateTest
        fields = ['date']

        widgets = {
            'date': DatePickerInput()
        }
