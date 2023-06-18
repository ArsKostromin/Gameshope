from distutils.command.upload import upload
from pyexpat import model
from tabnanny import verbose
from turtle import title
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
'''from datetime import date'''


class St(models.Model):
    title = models.CharField(max_length=35, help_text="Enter field documentation", verbose_name='название')
    img = models.ImageField(upload_to='images', null=True, blank=True, verbose_name='Картинка')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    genre = models.ForeignKey('Genre', null=True, on_delete=models.PROTECT, verbose_name='Жанр')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True, verbose_name='Издатель')
    buyers = models.ManyToManyField(User, verbose_name='Покупатели', blank=True)

    class Meta:
        verbose_name_plural = 'Игры'
        verbose_name = 'Игру'
        ordering = ['-published']

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('st-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='название')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'
        ordering = ['name']

class Publisher(models.Model):
    name = models.CharField(max_length=20, verbose_name='название', db_index=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('publisher-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Издатели'
        verbose_name = 'Издатель'
        ordering = ['name']

