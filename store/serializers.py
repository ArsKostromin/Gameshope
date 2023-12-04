from rest_framework import serializers
from store.models import St, Genre, Publisher, Review

class GameSerializer(serializers.ModelSerializer):
    published = serializers.ReadOnlyField(source='publisher.name')
    genre = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        model = St
        fields = ['title', 'content', 'price', 'published', 'genre', 'id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'id']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'id']