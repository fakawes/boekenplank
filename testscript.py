import os
from unicodedata import category
import django 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_boekenplank.settings')
django.setup()
from app_boekenplank.models import Book, BookReview, Category, Publisher, Category_test, Author
import datetime
from django.contrib.auth.models import User

from django.db.models import Count, Max



# return the 
def most_reviewed_books():
    
    # book_query_collection = Book.objects.values('title','id').annotate(num_reviews = Count('bookreview')).order_by('-num_reviews')
    book_query_collection = Book.objects.all()
    book_collection  = {}
    for book in book_query_collection:
        bookreviews = book.bookreview_set.filter(book=book)
        for review in bookreviews:
            
            if book.id in book_collection.keys():
                book_collection[book.id]['score'] += review.score    
                book_collection[book.id]['num_reviews'] += 1
            else:
                book_collection[book.id] = {}
                book_collection[book.id]['score'] = review.score
                book_collection[book.id]['num_reviews'] = 1             
    for book in book_collection.values():
        book['score'] = book['score'] / book['num_reviews']

    sortedDict = []
    
    book_collection = book_collection
    
    while book_collection:
        
        firstKey = list(book_collection.keys())[0]
        
        minScore = book_collection[firstKey]['score']
        
        for item in book_collection.items():
            
            if item[1]['score'] <= minScore:
                minScore = item[1]['score']
        
        sortedDict.append(item)        
        book_collection.pop(firstKey)
    
    #add book object to dict
    for i in sortedDict:
        key = i[0]
        value = i[1]
        
        book_object = Book.objects.get(pk=key)
        
        value['book_object'] = book_object
        
    return sortedDict
    # channels = book_collection.OrderedDict(sorted(channels.items(), key=lambda item: item[0]))
    
    # print(channels)
    # best_books = {}
    
    # for key,value in book_collection.items():
    #     print(key)
    #     book_object = Book.objects.get(key)
        
    #     if book_object not in best_books.keys():
    #         score = value['score']

    #     else:
    #         best_books[book_object] = value
    


def sort_test():
    
    list = [4,2,4,3,5,1]
    newList = []
    while list:
        #Pak eerste item
        min = list[0]
        
        for index, i in enumerate(list):              
            if i <= min:
                min = i
            print(i)
        newList.append(min)
        list.remove(min)
    
    print(newList)

def get_author():
    
    for i in Author.objects.all():
        
        print(i.id)
        print(i.image)

get_author()