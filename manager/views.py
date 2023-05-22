from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from config.utils import update_book_status
from manager.models import Book
from manager.serializer import BookSerializer, SpecificBookSerializer
from django.db.models import Q
from config.logger import log_warning
from config.celery_tasks import CeleryTasks


# Do we need 3 different views for this? How do you make it better?
# ViewSet (Retrive/List) --> Model --> Parse
# Filter --> Range library
# Pagination class

class BookDetailAPIView(APIView):

    def get(self, request):
        try:
            title = request.query_params.get('title')
            book = Book.objects.get(title=title)
            if not book.is_updated():
                update_book_status(book)
        except Book.DoesNotExist:
            log_warning(Book.DoesNotExist)
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = SpecificBookSerializer(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BookSearchAPIView(APIView):

    # Any idea how you can make this code cleaner?
    def get(self, request, *args, **kwargs):
        queryset = Book.objects.all()

        for field in ['title', 'author']:
            if value := request.GET.get(field):
                queryset = queryset.filter(**{f"{field}__icontains": value})

        pub_date_query = request.GET.get('pub_date')
        if pub_date_query:
            pub_dates = pub_date_query.split('_')
            if len(pub_dates) == 1:
                queryset = queryset.filter(publication_date__exact=pub_dates[0])
            elif len(pub_dates) == 2:
                queryset = queryset.filter(
                    publication_date__range=[pub_dates[0], pub_dates[1]]
                )

        # price_query = request.GET.get('price__start', 'price__end')
        price_query = request.GET.get('price')
        if price_query:
            prices = price_query.split('-')
            if len(prices) == 1:
                queryset = queryset.filter(price__exact=prices[0])
            elif len(prices) == 2:
                queryset = queryset.filter(price__range=[prices[0], prices[1]])

        subjects_query = request.GET.get('subjects')
        if subjects_query:
            subjects = subjects_query.split(',')
            filters = [Q(subjects__icontains=subject) for subject in subjects]
            queryset = queryset.filter(*filters)

        for book in queryset:
            if not book.is_updated():
                update_book_status(book)
        serializer = SpecificBookSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class BookList(generics.MoldeViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    # filter =
    # pagination_class =

    def list(self, request, *args, **kwargs):
        for book in self.get_queryset():
            if not book.is_updated():
                update_book_status(book)
        return super().list(request, *args, **kwargs)
