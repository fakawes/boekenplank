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
                book_collection[book.id]['avg_score'] = book_collection[book.id]['score'] / book_collection[book.id]['num_reviews']
            else:
                book_collection[book.id] = {}
                book_collection[book.id]['num_reviews'] = 1   
                book_collection[book.id]['score'] = review.score
                book_collection[book.id]['avg_score'] = review.score 
    
    sortedBooks = []
    
    #sorting method
    while book_collection:
        firstItem = list(book_collection.items())[0]
        #loop to check what the lowest book is
        for item in book_collection.items():
            if item[1]['score'] > firstItem[1]['score']:
                firstItem = item
        
        #add book_object to dict
        book_object = Book.objects.get(pk=firstItem[0])
        firstItem[1]['book'] = book_object
        
        sortedBooks.append(firstItem)
        book_collection.pop(firstItem[0])
    return sortedBooks
    
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
            book_collection[author_review.book.author.id][author_book_string]['avg_score'] = author_review.score
    
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

#return a random book of a author
def author_books():
    pass
    return 

