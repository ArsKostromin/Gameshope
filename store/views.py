from multiprocessing import context
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Publisher, St, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from cart.forms import CartAddProductForm
from django.urls import reverse
from django.views.generic.edit import FormMixin
from .forms import ReviewForm
from .utils import searchSt
from django.db.models import Q
from rest_framework.views import APIView
from store.serializers import GamePostSerializer, GameSerializer, GenreSerializer, PublisherSerializer
from rest_framework import permissions, renderers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from store.permissions import IsAdminOrSuperuser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet


class GenrePublisherYear:
    def get_publisher(self):
        return Publisher.objects.all()
    
    def get_genre(self):
        return Genre.objects.all()
    
    def get_published(self):
        return St.objects.values('published')
    

def by_genre(request, genre_slug):
    current_genre = get_object_or_404(Genre, slug=genre_slug)
    sss = St.objects.filter(genre=current_genre)
    genres = Genre.objects.all()
    cart_st_form = CartAddProductForm()
    context = {'sss': sss, 'genres': genres, 'current_genre': current_genre, 'cart_st_form': cart_st_form,}
    return render(request, 'store/by_genre.html', context)


class StoreListView(GenrePublisherYear, generic.ListView):
    model = St
    context_object_name = 'st_list'
    paginate_by = 4
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            queryset = St.objects.filter(title__icontains=query)
        else:
            queryset = St.objects.all().select_related('genre')
        return queryset


class StoreDetailView(FormMixin, generic.DetailView):
    model = St
    form_class = ReviewForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_st_form'] = CartAddProductForm()
        return context
    
    def get_success_url(self):
        return reverse('st-detail', kwargs={'slug': self.get_object().slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.get_object()
        self.object.owner = self.request.user.profile
        self.object.save()
        self.object.project.getVoteCount 
        return super().form_valid(form)


class PublisherDetailView(generic.DetailView):
    model = Publisher
    
    
class FilterGameView(GenrePublisherYear, generic.ListView):
    '''Фильтр игр'''
    def get_queryset(self):
        queryset = St.objects.filter(genre__in=self.request.GET.getlist('genre')).select_related('genre')
        return queryset


#дальше api
class GametViewSet(ModelViewSet):
    queryset = St.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, 
        IsAdminOrSuperuser]

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return GamePostSerializer
        return GameSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'genre__name', 'publisher__name']
    search_fields = ['title', 'genre__name', 'publisher__name']
    # permission_classes = [IsAdminOrSuperuser]

    def get_queryset(self):
        queryset = super().get_queryset()

        title = self.request.query_params.get('title', None)
        genre = self.request.query_params.get('genre', None)
        publisher = self.request.query_params.get('publisher', None)

        # Применение фильтров, если они заданы
        if title:
            queryset = queryset.filter(title=title)
        if genre:
            genre_obj = get_object_or_404(Genre, name=genre)
            queryset = queryset.filter(genre=genre_obj)

        if publisher:
            publisher_obj = get_object_or_404(Publisher, name=publisher)
            queryset = queryset.filter(publisher=publisher_obj)

        return queryset


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
