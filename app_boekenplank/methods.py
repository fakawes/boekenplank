from app_boekenplank.models import Book, BookReview, Category, Publisher, Category_test, Author
from django.db.models import Count

#return random review list of most review book
def most_reviewed_books():
    book_query_collection = Book.objects.values('title','id').annotate(num_reviews = Count('bookreview')).order_by('-num_reviews')[:3]
    book_collection  = []
    for book in book_query_collection:
        
        if book['num_reviews'] != 0:
            random_review = BookReview.objects.filter(book=book['id']).order_by('?').first()
            book_collection.append(random_review)
    
    return book_collection

#get book of each category, most red first
def category_books():
    category_table = Book.category.through.objects.all()
    category_collection = category_table.values('category_id').annotate(num_books=Count('category_id')).order_by('-num_books')
    category_best = {}
    for category in category_collection:    
        category_name = Category.objects.get(id=category['category_id'])
        
        random_book = Book.objects.filter(category=category_name).order_by('?').first()
        category_best[category_name] = random_book
    
    return category_best

#return a random book of a author
def author_books():
        
    book = None

    while book == None:
        author = Author.objects.filter().order_by('?').first()
        book = Book.objects.filter(author=author).first()
        
    return book