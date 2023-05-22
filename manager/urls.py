from django.urls import path

from manager.views import BookList, BookDetailAPIView, BookSearchAPIView

urlpatterns = [
    # is this a good pattern? How do you make it better?
    # JSON API https://jsonapi.org/

    # router('book/', BookSearchAPIView.as_view()),

    # path('book/', BookSearchAPIView.as_view()),
    # path('book/<id/uuid>/', BookDetailAPIView.as_view()),



    path('books/', BookList.as_view()),
    path('detail/', BookDetailAPIView.as_view()),
    path('search/', BookSearchAPIView.as_view()),
]
