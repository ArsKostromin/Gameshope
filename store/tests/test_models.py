from django.test import TestCase
from store.models import Publisher, St, Genre, Review
from users.models import Profile
import mock
from django.core.files import File
from django.contrib.auth.models import User




class PublisherModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Publisher.objects.create(name='Sony Interactive', slug='Sony')
    
    def test_get_absolute_url(self):
        publisher = Publisher.objects.get(name='Sony Interactive')
        self.assertEqual(publisher.get_absolute_url(), '/store/publisher-Sony')


class GameModelTest(TestCase):
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
        self.profile = Profile.objects.create(name='skuf', user=self.user_test1)
        self.review = Review.objects.create(owner=self.profile, project=self.one_game, value='452efds')
        
    def test_verbose_name(self):
        field_verboses = {
            'title': 'название',
            'img': 'Картинка',
            'content': 'Описание',
            'published': 'Опубликовано',
            'genre': 'Жанр',
            'publisher': 'Издатель',
            'buyers': 'Покупатели',
            'slug': 'URL'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                error_name = f'Поле {field} не ожидало значение {expected_value}'
                self.assertEqual(
                    self.one_game._meta.get_field(field).verbose_name,
                    expected_value, error_name)
                
    def test_st_creation(self):
        self.assertTrue(isinstance(self.one_game, St))
        self.assertEqual(self.one_game.__str__(), self.one_game.title)
        
    def test_genre_creation(self):
        self.assertTrue(isinstance(self.genre_test1, Genre))
        self.assertEqual(self.genre_test1.__str__(), self.genre_test1.name)
        
    def test_review_representation(self):
        review = self.review
        self.assertEqual(
            self.review.__str__(), self.review.value
        )