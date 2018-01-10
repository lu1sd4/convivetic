from django.urls import path, re_path

from django.contrib.auth import views as auth_views

from . import views

from .views import Index
from .views import Login
from .views import UsernameCheck
from .views import Forums
from .views import ForumDetail
from .views import PasswordReset
from .views import PasswordResetDone
from .views import PasswordResetConfirm
from .views import PasswordResetComplete




urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('signup', views.register_user, name='signup'),
	path('login', Login.as_view(), name='login'),
	path('logout', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
	path('api/users/<str:user_id>', UsernameCheck.as_view(), name='username_check'),
	path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
	path('password_reset_request/', PasswordReset.as_view(), name='password_reset_request'),
	path('password_reset_request_done/', PasswordResetDone.as_view(), name='password_reset_done'),
	path('password_reset_confirm/<uidb64>/<token>', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
	path('forums/', Forums.as_view(), name='forums'),
	path('forums/<int:pk>/', ForumDetail.as_view(), name="thread-detail")
]