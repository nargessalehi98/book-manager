import requests
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_date', 'price', 'cover_image_url')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        file_url = data.get('cover_image_url')
        if file_url:
            response = requests.get(file_url)
            if response.status_code == 200:
                data['file'] = response.content.decode(encoding='ISO-8859-1')
        return data


class SpecificBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
