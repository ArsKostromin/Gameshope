import pytest
from rest_framework import exceptions
from store.serializers import GamePostSerializer, GameSerializer, GenreSerializer, PublisherSerializer
from store.models import Publisher, St, Genre
from django.test import TestCase


class GameSerializerTest(TestCase):
    def setUp(self):
        self.publisher1 = Publisher.objects.create(name='test_publisher', slug='test_publisher_slug')
        self.genre1 = Genre.objects.create(name='test_genre', slug='test_genre_slug')
        # self.game = St.objects.create(title='test game', content="this is a test game", price=1500, slug='test', publisher=Publisher.objects.get(id=1), genre=Genre.objects.get(id=1))
        self.game_data = {
            "title": "test game name",
            "content": "this is a test game",
            "price": '1000',
            "slug": "test",
            "publisher": self.publisher1,
            "genre": self.genre1,
            'id': 1,
            'total_votes': 5,
            'votes_ratio': 4,
        }

    def test_game_serializer(self):
        # Создаем экземпляр сериализатора с тестовыми данными       
        serializer = GameSerializer(data=self.game_data)
        
        # Проверяем, что сериализатор валиден
        self.assertTrue(serializer.is_valid())

        # Создаем объект St на основе сериализатора
        game_instance = serializer.save()

        # Получаем данные из сериализатора
        serialized_data = serializer.data
        # print(self.game_data["publisher"])
        # print(serialized_data["publisher"])
        
        # Проверяем, что данные сериализатора соответствуют ожидаемым значениям
        self.assertEqual(serialized_data['title'], self.game_data['title'])
        self.assertEqual(serialized_data['content'], self.game_data['content'])
        self.assertEqual(serialized_data['price'], self.game_data['price'])
        self.assertEqual(serialized_data['id'], self.game_data['id'])
        self.assertEqual(serialized_data['slug'], self.game_data['slug'])
        self.assertEqual(serialized_data['total_votes'], self.game_data['total_votes'])
        self.assertEqual(serialized_data['votes_ratio'], self.game_data['votes_ratio'])



# def test_1():
#     serializer = GameSerializer(data={
#         "title": "test game name",
#         "content": "this is a test game",
#         "price": 500,
#         "slug": "test",
#         "publisher": test_publisher,
#         "genre": test_genre,
#     })
#     assert serializer.is_valid()
#     assert serializer.data == {
#         "title": "test game name",
#         "content": "this is a test game",
#         "price": 500,
#         "slug": "test",
#         "publisher": test_publisher,
#         "genre": test_genre,
#     }