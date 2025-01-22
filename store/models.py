from distutils.command.upload import upload
from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from users.models import Profile


class St(models.Model):
    title = models.CharField(max_length=35, help_text="Enter field documentation", verbose_name='название')
    img = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Картинка')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=0, default=None)
    published = models.DateField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    genre = models.ForeignKey('Genre', null=True, on_delete=models.PROTECT, verbose_name='Жанр')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, verbose_name='Издатель')
    buyers = models.ManyToManyField(User, verbose_name='Покупатели', blank=True)
    slug = models.SlugField(unique=True, verbose_name="URL", db_index=True)
    total_votes = models.IntegerField(default=0, null=True, blank=True)
    votes_ratio = models.IntegerField(default=0, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Игры'
        verbose_name = 'Игру'
        ordering = ['-published']

    #@property: Позволяет создавать свойства вместо методов.
    @property
    def reviewers(self):
        """
        Возвращает список идентификаторов всех владельцев (owner), которые оставили отзывы (review) для данного объекта.

        - Использует связанную модель `review_set` (задано через связь ForeignKey) для получения всех связанных отзывов.
        - Применяет `values_list` с аргументами ('owner__id', flat=True), чтобы извлечь только значения поля `id` из связанных объектов владельцев.
        - Преобразует результат в упрощенный список идентификаторов.

        Returns:
            QuerySet: Список идентификаторов владельцев отзывов.
        """
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset


    def display_genre(self):
        """Создает строку для жанра. Это необходимо для отображения жанра в Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к определенному экземпляру книги.
        """
        return reverse('st-detail', args={ self.slug })

    def __str__(self):
        """
        Строка для представления модельного объекта.
        """
        return self.title
    

class Genre(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='название')
    slug = models.SlugField(unique=True, verbose_name="URL", db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'
        ordering = ['name']

class Publisher(models.Model):
    name = models.CharField(max_length=20, verbose_name='название', db_index=True)
    slug = models.SlugField(unique=True, verbose_name="URL", db_index=True)

    def get_absolute_url(self):
        """
        Возвращает URL-адрес для доступа к конкретному экземпляру author.
        """
        return reverse('publisher-detail', args=[str(self.slug)])      

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Издатели'
        verbose_name = 'Издатель'
        ordering = ['name']


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Положительная оценка'),
        ('down', 'Отрицательная оценка'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(St, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]
        verbose_name_plural='Отзывы'
        verbose_name = 'От зыв'
        ordering = ('created',)

    def __str__(self):
        return self.value