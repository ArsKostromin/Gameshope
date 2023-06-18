from django.test import TestCase
from store.models import Publisher

class PublisherModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Publisher.objects.create(name='Wolf Dj')
    
    def test_get_absolute_url(self):
        publisher = Publisher.objects.get(id=1)
        self.assertEqual(publisher.get_absolute_url(), '/store/publisher1')


