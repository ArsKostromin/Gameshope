import factory
from store.models import Publisher, St, Genre, Review

class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre
    
    name = factory.Faker('sentence')
    slug = factory.Faker('slug')
    
class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher
    
    name = factory.Faker('sentence')
    slug = factory.Faker('slug')



class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = St
        
    title = factory.Faker('sentence')
    slug = factory.Faker('slug')
    content = factory.Faker('sentence')
    price = factory.Faker('random_int', min=0, max=10000)
    publisher = factory.SubFactory(PublisherFactory)
    genre = factory.SubFactory(GenreFactory)

