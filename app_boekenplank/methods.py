from random import random
from app_boekenplank.models import Book, BookReview, Category, Publisher, Category_test, Author
from django.db.models import Count

#return random review list of most review book
def most_reviewed_books():
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
        
        value['book'] = book_object
        
    return sortedDict
    

#get book of each category, most red first
def category_books():
    category_table = Book.category.through.objects.all()
    category_collection = category_table.values('category_id').annotate(num_books=Count('category_id')).order_by('-num_books')
    category_best = {}
    for category in category_collection:    
        category_name = Category.objects.get(id=category['category_id'])
    
        random_book = Book.objects.filter(category=category_name).order_by('?').first()
        random_review = BookReview.objects.filter(book=random_book).order_by('?').first()
        
        category_best[category_name] = {}
        category_best[category_name]['book'] = random_book
        category_best[category_name]['review'] = random_review
        
        
        # print(category_best.keys())
        
        
        # category_best[category_name]['review'] = BookReview.objects.filter(book=random_book).order_by('?').first()
    
    return category_best

#return a random book of a author
def author_books():
        
    # book = None

    # while book == None:
    #     author = Author.objects.filter().order_by('?').first()
    #     book = Book.objects.filter(author=author).first()
    
    author = Author.objects.get(pk=5)
    
    return author