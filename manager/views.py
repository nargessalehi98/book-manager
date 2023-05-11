from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from manager.models import Book
from manager.serializer import BookSerializer
from django.db.models import Q


class BookDetailAPIView(APIView):

    def get(self, request):
        try:
            title = request.query_params.get('title')
            book = Book.objects.get(title=title)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class BookSearchAPIView(APIView):

    def get(self, request, *args, **kwargs):
        queryset = Book.objects.all()

        for field in ['title', 'author']:
            if value := request.GET.get(field):
                queryset = queryset.filter(**{f"{field}__icontains": value})

        pub_date_query = request.GET.get('pub_date')
        if pub_date_query:
            pub_dates = pub_date_query.split('-')
            if len(pub_dates) == 1:
                queryset = queryset.filter(publication_date__exact=pub_dates[0])
            elif len(pub_dates) == 2:
                queryset = queryset.filter(
                    publication_date__range=[pub_dates[0], pub_dates[1]]
                )

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

        serializer = BookSerializer(instance=queryset, many=True)
        return Response(serializer.data)


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
