"""project_boekenplank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from app_boekenplank import views
from django.urls import include,path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(), name='index' ),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('add_books/', views.AddBooks.as_view(), name='add_books'),
    path('accounts/', include('allauth.urls')),
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/edit', views.EditAccountView.as_view(), name='edit-account'),
    path('book/<int:pk>/', views.BookView.as_view()),
    path('review/<int:pk>/', views.BookReviewView.as_view()),
    path('review/edit/<int:pk>/', views.EditReviewView.as_view()),
    
    path('author/<int:pk>/', views.AuthorView.as_view()),
    path('datepicker/', views.DatePickerView.as_view(), name='datepicker'),
    path('review/<int:comment_id>/<str:opition>', views.UpdateCommentVote.as_view(), name='review_comment_vote'),

    
]
handler404 = "app_boekenplank.views.page_not_found_view"
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

