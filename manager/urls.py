from django.urls import path

from manager.views import BookList, BookDetailAPIView, BookSearchAPIView

urlpatterns = [
    path('books/', BookList.as_view()),
    path('detail/', BookDetailAPIView.as_view()),
    path('search/', BookSearchAPIView.as_view()),
]
