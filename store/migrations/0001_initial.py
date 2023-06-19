# Generated by Django 4.1.7 on 2023-06-19 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='название')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=20, verbose_name='название')),
            ],
            options={
                'verbose_name': 'Издатель',
                'verbose_name_plural': 'Издатели',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='St',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter field documentation', max_length=35, verbose_name='название')),
                ('img', models.ImageField(blank=True, null=True, upload_to='images', verbose_name='Картинка')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=0, default=None, max_digits=10)),
                ('published', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')),
                ('buyers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Покупатели')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='store.genre', verbose_name='Жанр')),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.publisher', verbose_name='Издатель')),
            ],
            options={
                'verbose_name': 'Игру',
                'verbose_name_plural': 'Игры',
                'ordering': ['-published'],
            },
        ),
    ]
