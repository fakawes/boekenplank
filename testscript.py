import os
from unicodedata import category
import django 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_boekenplank.settings')
django.setup()
from app_boekenplank.models import Book, BookReview, Category, Publisher, Category_test, Author
import datetime
from django.contrib.auth.models import User

from django.db.models import Count, Max



book = None

while book == None:
    author = Author.objects.filter().order_by('?').first()
    book = Book.objects.filter(author=author).first()
print(book)
    

# for i in Book.objects.all():
    
#     category_list = i.category.values('name').annotate(num_categories=Count('name')).order_by('num_categories')
    
#     print(category_list)
#     for category in category_list:
#         name = category['name']
#         count = category['num_categories']
#         print(count)
        

#         # best_category[name] = 

# print(best_category)

# book_query_collection = list(Book.objects.values('title','id').annotate(num_reviews = Count('bookreview')).order_by('-num_reviews'))


# category_list = i.category.values('name').annotate(num_categories=Count('name')).order_by('num_categories')

# #check if amout of reviews nog null
# book_collection  = []
# for i in book_query_collection:
#     bookTitle = i['title']
#     num_reviews = i['num_reviews']
#     book_id = i['id']
    
#     if num_reviews != 0:
#         print(i)
#         random_review = BookReview.objects.filter(book=book_id).order_by('?').first()
#         book_collection.append(random_review)

# print(book_collection)