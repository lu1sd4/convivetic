from django.urls import path, re_path

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

from .views import *

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
	path('forums/<int:pk>/', ForumDetail.as_view(), name="thread-detail"),
	path('forums/<int:pk>/vote', login_required(ForumLike.as_view()), name="forum-like"),
	path('forums/<int:pk>/unvote', ForumDislike.as_view(), name="forum-dislike"),
	path('forums/<int:pk>/view', ForumView.as_view(), name="forum-view"),
	path('forums/<int:pk>/comment/<str:content>', login_required(ForumComment.as_view()), name="forum-comment")

]