from importlib.resources import contents
from msilib.schema import Class
from multiprocessing import context
from urllib import request
from webbrowser import get
from django.shortcuts import redirect, render
#forms
from app_boekenplank.form import BookForm, ReviewForm, AuthorForm, PublisherForm, CategoryForm, contactForm, newsLetterForm, editAccountForm
from app_boekenplank.models import Book,BookReview, Author, Category, Publisher, Author

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from django.views.generic.edit import FormView,CreateView
from django.views.generic import View
from django.views.generic import TemplateView
from django.db.models import Count

#custom methods
from app_boekenplank.methods import most_reviewed_books, category_books, author_books, get_author


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



# MAAK HIER EEN FORM VIEW VAN
class CreateCategoryView(CreateView):
    template_name = 'forms/form_test.html'
    form_class = CategoryForm
    success_url = '/test/'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class AccountView(LoginRequiredMixin,TemplateView):
    template_name = 'account.html'
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

class EditAccountView(View, LoginRequiredMixin):
    
    template_name='edit_account.html'
    
    def get_context_data(self, *args, **kwargs):
        print('\n --> get context DATA')
        
        if editAccountForm not in kwargs.keys():
            kwargs['editAccountForm'] = editAccountForm(instance=self.request.user)
        
        return kwargs
    
    def get(self, request, *args, **kwargs):
        print('\n--> GET' )
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
    
# MAAK HIER EEN FORM VIEW VAN
class AddBooks(View, LoginRequiredMixin):

    template_name = 'forms/add_books.html'
    success_url = 'forms/add_books.html'
    
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
        print(request.POST)
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
            print('--> add Author form')
            form  = AuthorForm(request.POST,request.FILES)

            if form.is_valid():
                print('--> FORM VALID')
                form.save()
                return redirect('/add_books')
            else:
                print('--> INVALID')
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
   