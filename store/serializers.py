from rest_framework import serializers
from store.models import St, Genre, Publisher, Review

class GameSerializer(serializers.ModelSerializer):
    published = serializers.ReadOnlyField(source='publisher.name')
    genre = serializers.ReadOnlyField(source='genre.name')

    class Meta:
        model = St
        fields = ['title', 'content', 'price', 'published', 'genre', 'id', 'slug', 'total_votes', 'votes_ratio']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'id']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['name', 'id']

class GamePostSerializer(serializers.ModelSerializer):
    publisher = serializers.SlugRelatedField(slug_field='slug', queryset=Publisher.objects.all())
    genre = serializers.SlugRelatedField(slug_field='slug', queryset=Genre.objects.all())

    class Meta:
        model = St
        fields = ['title', 'content', 'price', 'slug','publisher', 'genre', 'img']