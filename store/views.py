from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import Publisher, St, Genre
from django.views import generic
from django.urls import reverse
from django.views.generic.edit import FormMixin
from .forms import ReviewForm
from cart.forms import CartAddProductForm
from store.serializers import GamePostSerializer, GameSerializer, GenreSerializer, PublisherSerializer
from rest_framework import permissions, filters, status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from store.permissions import IsAdminOrSuperuser
from .task import update_vote_count
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .services import (
    get_all_publishers, get_all_genres, get_all_published_years,
    filter_games_by_title, filter_games_by_genre, get_games_by_genre, create_review, get_games_by_publisher
)

#для отображения жанров на боковой панели итд
class GenrePublisherYear:
    def get_publisher(self):
        return get_all_publishers()

    def get_genre(self):
        return get_all_genres()

    def get_published(self):
        return get_all_published_years()
    

def by_genre(request, genre_slug):
    sss, current_genre = get_games_by_genre(genre_slug)
    cart_st_form = CartAddProductForm()
    context = {'sss': sss, 'current_genre': current_genre, 'cart_st_form': cart_st_form}
    return render(request, 'store/by_genre.html', context)


class StoreListView(GenrePublisherYear, generic.ListView):
    model = St
    context_object_name = 'st_list'
    paginate_by = 4
    #фильтрация по названию и жанру игры
    def get_queryset(self):
        query = self.request.GET.get('query')
        return filter_games_by_title(query)


# Детальная информация о товаре + форма отзыва
class StoreDetailView(FormMixin, generic.DetailView):
    model = St
    form_class = ReviewForm
    
    def get_context_data(self, **kwargs):
        # Получаем базовый контекст из родительского класса
        context = super().get_context_data(**kwargs)
        
        # Добавляем в контекст форму для добавления товара в корзину
        context['cart_st_form'] = CartAddProductForm()
        
        # Возвращаем обновленный контекст
        return context

    
    def get_success_url(self):
        # Возвращаем URL для перенаправления после успешного выполнения действия.
        # Используем reverse для построения URL, подставляя slug текущего объекта
        # (полученного с помощью self.get_object()), чтобы перенаправить пользователя
        # на детальную страницу этого объекта ('st-detail').
        return reverse('st-detail', kwargs={'slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid

    def form_valid(self, form):
        create_review(form, self.get_object(), self.request.user)
        return super().form_valid(form)


class PublisherDetailView(generic.DetailView):
        # Используем prefetch_related для оптимизации запросов:
        # Подгружаем связанные объекты St (st_set) и их жанры (genre) для каждого Publisher
        # Это позволяет избежать проблемы N+1 запросов, выполняя отдельный запрос для связанных объектов.
    model = Publisher
    def get_queryset(self):
        return get_games_by_publisher()
    
    
# Фильтрация игр по жанру
class FilterGameView(GenrePublisherYear, generic.ListView):
    def get_queryset(self):
        genres = self.request.GET.getlist('genre')
        return filter_games_by_genre(genres)


#дальше api
class GametViewSet(ModelViewSet):
    queryset = St.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsAdminOrSuperuser]
    
    @swagger_auto_schema(
        operation_description="Получить список игр",
        responses={200: GameSerializer(many=True)},
    )

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return GamePostSerializer
        return GameSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter] # указываем что будет использоваться для фильтрации и поиска
    filterset_fields = ['title', 'genre__name', 'publisher__name'] # поля для фильтрации
    search_fields = ['title', 'genre__name', 'publisher__name'] # поля для поиска(менее точного)

    # def get_queryset(self): # Ручная реализация DjangoFilterBackend
    #     queryset = super().get_queryset()

    #     title = self.request.query_params.get('title', None)
    #     genre = self.request.query_params.get('genre', None)
    #     publisher = self.request.query_params.get('publisher', None)

    #     # Применение фильтров, если они заданы
    #     if title:
    #         queryset = queryset.filter(title=title)
    #     if genre:
    #         genre_obj = get_object_or_404(Genre, name=genre)
    #         queryset = queryset.filter(genre=genre_obj)

    #     if publisher:
    #         publisher_obj = get_object_or_404(Publisher, name=publisher)
    #         queryset = queryset.filter(publisher=publisher_obj)

    #     return queryset


class GetGenreInfoView(APIView): 
    def get(self, request):
        queryset = Genre.objects.all()
        serializer_context = {'request': request}
        serializer_class = GenreSerializer(
            instance=queryset,
            many=True,
            context=serializer_context
        )
        return Response(serializer_class.data)


class GetPublisherInfoView(APIView):
    def get(self, request):
        queryset = Publisher.objects.all()
        serializer_context = {'request': request}
        serializer_class = PublisherSerializer(
            instance=queryset,
            many=True,
            context=serializer_context
        )
        return Response(serializer_class.data)
