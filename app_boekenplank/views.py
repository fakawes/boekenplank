from importlib.resources import contents
from msilib.schema import Class
from multiprocessing import context
from urllib import request
from webbrowser import get
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django import forms
#forms
from app_boekenplank.form import BookForm, ReviewForm, AuthorForm, PublisherForm, CategoryForm, contactForm, newsLetterForm, editAccountForm,ReviewCommentForm
from app_boekenplank.models import Book,BookReview, Author, Category, Publisher, Author, ReviewComment

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic.edit import FormView,CreateView
from django.views.generic import View
from django.views.generic import TemplateView, DetailView
from django.db.models import Count

#custom methods
from app_boekenplank.methods import most_reviewed_books, category_books, author_books, get_author

from bootstrap_datepicker_plus.widgets import DateTimePickerInput
#View for the index

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def get_context_data(self, **kwargs):
        kwargs['book_collection'] = most_reviewed_books()
        kwargs['category_collection'] = category_books()
        kwargs['author'] = get_author()
        
        if 'newsLetterForm' not in kwargs.keys():
            kwargs['newsLetterForm'] = newsLetterForm()
        return kwargs
    
    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'newsLetterForm' in request.POST:
            form = newsLetterForm(request.POST)
            if form.valid:
                return redirect('/')
            else:
                context['newsLetterForm'] = form
        
        return render(request,self.template_name, self.get_context_data(**context))   

#view for a specific book
class BookView(DetailView):
    template_name = 'book.html'
    
    context_object_name = 'book'
    model = Book
    def get_context_data(self, **kwargs):
        
        # context = super().get_context_data(**kwargs)
        book = super(BookView,self).get_object()
        book_reviews = BookReview.objects.filter(book = book)
        
        
        kwargs['comment_collection'] = book_reviews
        # print(book_reviews)
        # context['now'] = timezone.now()
        return kwargs
    
    def post(self, request, *args, **kwargs):
        print('--> nu is er een post request')
#view for a specific review
class BookReviewView(DetailView):
    template_name = 'review.html'
    context_object_name = 'book'
    model = BookReview
    # def get_queryset(self):        
    #     queryset = BookReview.objects.filter(user=self.request.user)
    #     return queryset
    def get_context_data(self, **kwargs):
        #pak het opject waar op geklikt wordt
        review_object = super(BookReviewView,self).get_object()
        
        if review_object.user == self.request.user:
            kwargs['edit_review'] = True
        
        if 'ReviewCommentForm' not in kwargs.keys():
            kwargs['ReviewCommentForm'] = ReviewCommentForm()
            # kwargs['ReviewCommentForm'].fields['review'].widget = forms.HiddenInput()
            # kwargs['ReviewCommentForm'].fields['user'].widget = forms.HiddenInput()
        
        
        
        
        kwargs['comment_collection'] = ReviewComment.objects.filter(review=review_object)
        
        return kwargs
    
    def post(self, request, *args, **kwargs):
        context = {}
        if 'ReviewCommentForm' in request.POST:
        
            form = ReviewCommentForm(request.POST)
        
            if form.is_valid:
                print('\n--> form Valid')     
                form_object = form.save(commit=False)
                form_object.user = self.request.user
                form_object.review = super(BookReviewView,self).get_object()    
                form_object.save()
                url = '/review/{}'.format(super(BookReviewView,self).get_object().id)
                return redirect(url)
                
            else:
                print('\n --> Not VALID')


#view for a specific author    
class AuthorView(DetailView):
    template_name = 'author.html'
    context_object_name = 'author'
    model = Author
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        author = super(AuthorView,self).get_object()
        book_collection = Book.objects.filter(author=author)
        context['book_collection'] = book_collection
        return context
    
#view for a the about page    
class AboutView(TemplateView):
    template_name = 'about.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def get_context_data(self, **kwargs):
        if 'newsLetterForm' not in kwargs.keys():
            kwargs['newsLetterForm'] = newsLetterForm()

        return kwargs

    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'newsLetterForm' in request.POST:
            form = newsLetterForm(request.POST)
            if form.valid:
                return redirect('/')
            else:
                context['newsLetterForm'] = form
        
        return render(request,self.template_name, self.get_context_data(**context))   
    
class EditReviewView(LoginRequiredMixin, DetailView):
    template_name = 'edit_review.html'
    def get_queryset(self):        
        queryset = BookReview.objects.filter(user=self.request.user)
        return queryset
    def get_context_data(self, *args, **kwargs):        
        review = super().get_object()        
        if 'add_review_form' not in kwargs.keys():
            kwargs['add_review_form'] = ReviewForm(instance=review)
            kwargs['add_review_form'].fields['book'].widget = forms.HiddenInput()
            kwargs['review'] = review
        return kwargs
        
    def post(self, request, *arg, **kwargs):
        context = {}
        review = super().get_object()        
        if 'add_review_form' in request.POST:

            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
            
                form.save()
                return redirect('/account')
            else:
                context['add_review_form'] = form
            
        return render(request,self.template_name, self.get_context_data(**context))   
#View for the Contact page
class ContactView(TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def get_context_data(self, **kwargs):
        if 'newsLetterForm' not in kwargs.keys():
            kwargs['newsLetterForm'] = newsLetterForm()
        if 'contactForm' not in kwargs.keys():
            kwargs['contactForm'] = contactForm()

        return kwargs

    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'newsLetterForm' in request.POST:
            form = newsLetterForm(request.POST)
            if form.valid:
                return redirect('/')
            else:
                context['newsLetterForm'] = form
        
        if 'contactForm' in request.POST:
            form = contactForm(request.POST)
            if form.valid:
                return redirect('/')
            else:
                context['contactForm'] = form
        
        return render(request,self.template_name, self.get_context_data(**context))   


#view for a account
class AccountView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    template_name = 'account.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
    
        kwargs['review_collection'] = BookReview.objects.filter(user=self.request.user)
    
        if 'newsLetterForm' not in kwargs.keys():
            kwargs['newsLetterForm'] = newsLetterForm()
        return kwargs

    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'newsLetterForm' in request.POST:
            form = newsLetterForm(request.POST)
            if form.valid:
                return redirect('/')
            else:
                context['newsLetterForm'] = form
        return render(request,self.template_name, self.get_context_data(**context))   

#View to edit account settings
class EditAccountView(LoginRequiredMixin, View ):
    template_name='edit_account.html'
    def get_context_data(self, *args, **kwargs):
        print('--> edit account')
        if editAccountForm not in kwargs.keys():
            print('editAccountForm')
            print(self.request.user)
            kwargs['editAccountForm'] = editAccountForm(instance=self.request.user)
        return kwargs
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    def post(self, request, *arg, **kwargs):
        context = {}
        if 'editAccountForm' in request.POST:
            print('\n -->>editAccountForm IS INT ')
            form = editAccountForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/account')
                
            else:
                print('\n --> NOT' )
        return render(request,self.template_name,self.get_context_data(**context))
    
#View to add Books
class AddBooks(LoginRequiredMixin ,View):
    template_name = 'add_books.html'
    success_url = 'add_books.html'    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
    
    # Check if the rededirect comes from Write book Review Page
    def get_context_data(self,**kwargs):
    
        if 'add_review_form' not in kwargs.keys():
            kwargs['add_review_form'] = ReviewForm()
            
        if 'add_book_form' not in kwargs.keys():     
            kwargs['add_book_form'] = BookForm()       
            
        if 'add_author_form' not in kwargs.keys():
            kwargs['add_author_form'] = AuthorForm()
            
        if 'add_publisher_form' not in kwargs.keys():                
            kwargs['add_publisher_form'] = PublisherForm()

        if 'newsLetterForm' not in kwargs.keys():
            kwargs['newsLetterForm'] = newsLetterForm()
        return kwargs
    
    #save the form that is sumbitted    
    def post(self, request, *args, **kwargs):
        context = {}
        if 'add_review_form' in request.POST:
            form  = ReviewForm(request.POST)
            if form.is_valid():            
                review = form.save(commit=False)
                review.user = self.request.user
                review.save()
                return redirect('/add_books')
            else:
                context['add_review_form'] = form
        
        if 'add_book_form' in request.POST:
            form  = BookForm(request.POST,request.FILES)
            
            if form.is_valid():
                form.save()
                return redirect('/add_books')
            else:
                context['add_book_form'] = form
        
        if 'add_author_form' in request.POST:
            
            form  = AuthorForm(request.POST,request.FILES)

            if form.is_valid():
            
                form.save()
                return redirect('/add_books')
            else:
            
                context['add_author_form'] = form
        if 'add_publisher_form' in request.POST:            
            form  = PublisherForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/add_books')
            else:
                context['add_publisher_form'] = form
        if 'newsLetterForm' in request.POST:
            form = newsLetterForm(request.POST)
            if form.valid:
                return redirect('/')
            else:
                context['newsLetterForm'] = form
        return render(request,self.template_name, self.get_context_data(**context))        
#View to login 
class LoginView(TemplateView):
    template_name='login.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        if 'newsLetterForm' not in kwargs.keys():
            kwargs['newsLetterForm'] = newsLetterForm()
        return kwargs

    def post(self, request, *args, **kwargs):
        context = {}
        
        if 'newsLetterForm' in request.POST:
            form = newsLetterForm(request.POST)
            if form.valid:
                return redirect('/')
            else:
                context['newsLetterForm'] = form
        return render(request,self.template_name, self.get_context_data(**context))   
   

class DatePickerView(TemplateView):
    template_name = 'datepicker.html'
    
    
    def get_context_data(self, **kwargs):
        context = {}
        
        context['add_author_form'] = DateForm()
        
        context['add_author_form'].fields['date'].widget = DateTimePickerInput()
        
        return context


class UpdateCommentVote(View):
    print('\n --> JA DE LINK werkt')

def page_not_found_view(request, exception):
    response = render(request, '404.html')    
    response.status_code = 404
    return response