from django.urls import path

from django.contrib.auth import views as auth_views

from .views import Index
from .views import Login

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('login', Login.as_view(), name='login'),
	path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout')
]