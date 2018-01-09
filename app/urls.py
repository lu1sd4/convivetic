from django.urls import path, re_path

from django.contrib.auth import views as auth_views

from . import views

from .views import Index
from .views import Login
<<<<<<< HEAD
from .views import UsernameCheck
=======
from .views import Forums
>>>>>>> f59eda76ab49b2723942faef6f2a4fbe6ba1afaa


urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('signup', views.register_user, name='signup'),
	path('login', Login.as_view(), name='login'),
	path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
	path('api/users/<str:user_id>', UsernameCheck.as_view(), name='username_check'),
	path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
	path('forums', Forums.as_view(), name='forums')
]