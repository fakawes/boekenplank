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
    
    book_query_collection = Book.objects.all()
    book_collection  = {}
    for book in book_query_collection:
        bookreviews = book.bookreview_set.filter(book=book)
        for review in bookreviews:
            
            if book.id in book_collection.keys():
                book_collection[book.id]['score'] += review.score    
                book_collection[book.id]['num_reviews'] += 1
                book_collection[book.id]['avg_score'] = book_collection[book.id]['score'] / book_collection[book.id]['num_reviews']
            else:
                book_collection[book.id] = {}
                book_collection[book.id]['score'] = review.score
                book_collection[book.id]['num_reviews'] = 1             
    
    sortedDict = []
    
    #sorting method
    while book_collection:
        
        firstKey = list(book_collection.keys())[0]
        
        minScore = book_collection[firstKey]['score']
        
        for item in book_collection.items():
            
            if item[1]['score'] <= minScore:
                minScore = item[1]['score']
        
        #add book_object to dict
        book_object = Book.objects.get(pk=item[0])
        item[1]['book'] = book_object
        
        sortedDict.append(item)
                
        book_collection.pop(firstKey)
        
    return sortedDict

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

def get_author():
    
    author = BookReview.objects.filter(book__author__isnull=False).order_by('?').first().book.author
    # author = book_review.book.author
    # author_review_query_collection = BookReview.objects.filter(book__author=author)
    book_collection  = {}
    
    author_review_query_collection = BookReview.objects.filter(book__author=author)
    
    for author_review in author_review_query_collection:
        author_book_string = f'author_book; {author_review.book.id}'
        
        if author_review.book.author.id in book_collection.keys():
            #edit total score of author
            book_collection[author_review.book.author.id]['author_score'] += author_review.score    
            book_collection[author_review.book.author.id]['num_reviews'] += 1
            book_collection[author_review.book.author.id]['avg_author_score'] = book_collection[author_review.book.author.id]['author_score'] / book_collection[author_review.book.author.id]['num_reviews']
            
            #edit each book for author
            book_collection[author_review.book.author.id][author_book_string]['score'] += author_review.score
            book_collection[author_review.book.author.id][author_book_string]['num_score'] += 1
            book_collection[author_review.book.author.id][author_book_string]['avg_score'] = book_collection[author_review.book.author.id][author_book_string]['score'] / book_collection[author_review.book.author.id][author_book_string]['num_score']
        else:
            #information about author
            book_collection[author_review.book.author.id] = {}
            book_collection[author_review.book.author.id]['author_score'] = author_review.score 
            book_collection[author_review.book.author.id]['avg_author_score'] = author_review.score 
            book_collection[author_review.book.author.id]['num_reviews'] = 1
            
            #add each book for author     
            book_collection[author_review.book.author.id][author_book_string] = {}
            book_collection[author_review.book.author.id][author_book_string]['book'] = author_review.book
            book_collection[author_review.book.author.id][author_book_string]['score'] = author_review.score
            book_collection[author_review.book.author.id][author_book_string]['num_score'] = 1
    
    firstKey = list(book_collection.keys())[0]
    authorBooks = []
    #add book of author to list
    for key in book_collection[firstKey].keys():
        if 'author_book;' in key:
            authorBooks.append(book_collection[firstKey][key])

    sorted_books = []
    while authorBooks:
        minScore = authorBooks[0]['avg_score']
        
        for book in authorBooks:
            
            if book['avg_score'] <= minScore:
                
                minScore = book['avg_score']
            
            sorted_books.append(book)
            authorBooks.remove(book)
    return sorted_books[0]

get_author()