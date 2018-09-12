from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView, CreateView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render

from .models import Playlist
from .forms import AddPlaylistForm


class SignUpView(TemplateView):
    template_name = 'signup.html'

    def dispatch(self, request, *args, **kwargs):
        self.form = UserCreationForm()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        c = super().get_context_data(**kwargs)
        c.update({
            'form': self.form
        })
        return c

    def post(self, request, *args, **kwargs):
        self.form = UserCreationForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            username = self.form.cleaned_data.get('username')
            raw_password = self.form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        return render(request, self.template_name, self.get_context_data(**kwargs))


class PlaylistsView(LoginRequiredMixin, ListView):
    model = Playlist
    template_name = 'playlists.html'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)


class AddPlaylistView(LoginRequiredMixin, CreateView):
    form_class = AddPlaylistForm
    template_name = 'add_playlist.html'

    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse('playlists')

    def get_form_kwargs(self):
        k = super().get_form_kwargs()
        k.update({'user': self.request.user})
        return k