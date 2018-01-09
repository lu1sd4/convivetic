from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

from .views import Index
from .views import Login
from .views import Forums


urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('signup', views.register_user, name='signup'),
	path('login', Login.as_view(), name='login'),
	path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
	path('forums', Forums.as_view(), name='forums')
]