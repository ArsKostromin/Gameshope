from multiprocessing import context
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




def by_genre(request, genre_id):
    sss = St.objects.filter(genre=genre_id)
    genres = Genre.objects.all()
    current_genre = Genre.objects.get(pk=genre_id)
    cart_st_form = CartAddProductForm()
    context = {'sss': sss, 'genres': genres, 'current_genre': current_genre, 'cart_st_form': cart_st_form,}
    return render(request, 'store/by_genre.html', context)

class StoreListView(generic.ListView):
    model = St
    context_object_name = 'sss'
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

class StoreDetailView(FormMixin, generic.DetailView):
    model = St
    form_class = ReviewForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
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
        return super().form_valid(form)

class PublisherDetailView(generic.DetailView):
    model = Publisher
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context

class LoanedStsByUserListView(LoginRequiredMixin,generic.ListView):
    model=St
    template_name = 'store\st_list_borrowed_user.html'
    paginate_by=10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        return context
    def get_queryset(self):
        return St.objects.filter(buyers=self.request.user)


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"