import mock
import json
from django.core.files import File
from django.contrib.auth.models import User
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from store.models import Publisher, St, Genre

class GameTests(APITestCase):
    def setUp(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'photo.png'
        self.publisher_test1 = Publisher.objects.create(name='test_publisher', slug='test_publisher_slug')
        self.genre_test1 = Genre.objects.create(name='test_genre', slug='test_genre_slug')
        self.one_game = St.objects.create(
            title="test game name",
            img=file_mock.name,
            content="this is a test game",
            price=1000,
            slug="test",
            publisher=self.publisher_test1,
            genre=self.genre_test1,
            id=1,
            total_votes=5,
            votes_ratio=4,
        )

        self.user_test1 = User.objects.create_superuser(username='test', email='sobaka@gmail.com', password='q1w2e3')
        self.user_test1.save()
        self.user_test2 = User.objects.create_user(username='test2', password='123qwerg')
        
        
        self.data = {
            "title": "new game title",
            "content": "this is a new test game",
            "price": 1500,  
            "slug": "new-test",  
            "publisher": Publisher.objects.create(name='new_test_publisher', slug='new_test_publisher'),
            "genre": Genre.objects.create(name='new_test_genre', slug='new_test_genre'),
        }
        
        self.user_test1_token = Token.objects.create(user=self.user_test1)
        self.user_test2_token = Token.objects.create(user=self.user_test2)


    def test_game_list(self):
        response = self.client.get(reverse('game-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_fail_game_detail(self):
        response = self.client.get(reverse('game-detail', kwargs={'pk': 50}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_game_detail(self):
        response = self.client.get(reverse('game-detail', kwargs={'pk': self.one_game.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), "test game name")
        
    def test_create_invalid_game(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_test2_token.key}')
        response = self.client.post(reverse('game-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_create_valid_game(self): 
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_test1_token.key}') 
        response = self.client.post(reverse('game-list'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 

    def test_user_is_staff(self):
        self.assertEqual(self.user_test1.is_staff, True)
        
    def test_publisher(self):
        response = self.client.get(reverse('APIpublisher'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_genre(self):
        response = self.client.get(reverse('APIgenre'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
