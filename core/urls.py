from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup', views.SignUpView.as_view(), name='signup'),
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('playlists', views.PlaylistsView.as_view(), name='playlists'),
    path('add-playlist', views.AddPlaylistView.as_view(), name='add_playlist'),
]
