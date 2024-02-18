from django.test import TestCase
from django.urls import reverse
from store.models import Publisher, St, Genre, Review
from .game_factories import GameFactory, GenreFactory, PublisherFactory


class GameViewsTest(TestCase):
    
    def test_game_list(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/st_list.html')
        
    def test_game_list2(self):
        game = GameFactory.create()
        response = self.client.get(game.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/st_detail.html')
        self.assertContains(response, game.title)

    def test_game_share_view(self):
        """
        Test for post share view
        """
        game = GameFactory.create()
        response = self.client.get(
            reverse('st-detail', kwargs={'slug': game.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, game.title)
        self.assertTemplateUsed(response, 'store/st_detail.html')
    
    def test_genre_list(self):
        genre = GenreFactory.create()
        response = self.client.get(reverse('by_genre', kwargs={'genre_slug': genre.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/by_genre.html')
        
    def test_publisher_list(self):
        publisher = PublisherFactory.create()
        response = self.client.get(reverse('publisher-detail', kwargs={'slug': publisher.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/publisher_detail.html')