from django.test import TestCase
from store.models import Publisher

class PublisherModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Publisher.objects.create(name='Sony Interactive', slug='Sony')
    
    def test_get_absolute_url(self):
        publisher = Publisher.objects.get(name='Sony Interactive')
        self.assertEqual(publisher.get_absolute_url(), '/store/publisher-Sony')


