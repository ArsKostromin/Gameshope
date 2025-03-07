from .models import Publisher, St, Genre
from store.task import update_vote_count

# Получение списка жанров, издателей и годов публикации
def get_all_publishers():
    return Publisher.objects.all()

def get_all_genres():
    return Genre.objects.all()

def get_all_published_years():
    return St.objects.values('published')

#фильтрация списка
def filter_games_by_title(query):
    '''фильтр по названию'''
    return St.objects.filter(title__icontains=query) if query else St.objects.all().select_related('genre')

def filter_games_by_genre(genres):
    """Фильтрация игр по жанру"""
    return St.objects.filter(genre__in=genres).select_related('genre') if genres else St.objects.all().select_related('genre')


def get_games_by_genre(genre_slug):
    """Получение списка игр по жанру"""
    current_genre = Genre.objects.get(slug=genre_slug)
    return St.objects.filter(genre=current_genre).select_related('genre'), current_genre

def create_review(form, project, user):
    """Создание отзыва и обновление голосов"""
    review = form.save(commit=False)
    review.project = project
    review.owner = user.profile
    review.save()
    update_vote_count.delay(project.id)
    return review

def get_games_by_publisher():
    return Publisher.objects.prefetch_related('st_set__genre')