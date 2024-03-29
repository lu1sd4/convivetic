from django.urls import path, re_path

from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from . import views

from .views import *

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('signup', views.register_user, name='signup'),
	path('login', Login.as_view(), name='login'),
	path('logout', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
	path('api/users/<str:user_id>', UsernameCheck.as_view(), name='username_check'),
	path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
	path('password_reset_request/', PasswordReset.as_view(), name='password_reset_request'),
	path('password_reset_request_done/', PasswordResetDone.as_view(), name='password_reset_done'),
	path('password_reset_confirm/<uidb64>/<token>', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
	path('password_reset_complete/', PasswordResetComplete.as_view(), name='password_reset_complete'),
	path('forums/', Forums.as_view(), name='forums'),
	path('forums/<str:order>', Forums.as_view(), name="forums-ordered"),
	path('forums/<int:pk>/', ForumDetail.as_view(), name="thread-detail"),
	path('forums/<int:pk>/like', login_required(ForumLike.as_view()), name="forum-like"),
	path('forums/<int:pk>/dislike', login_required(ForumDislike.as_view()), name="forum-dislike"),
	path('forums/<int:pk>/removeLike', login_required(ForumRemoveLike.as_view()), name="forum-removelike"),
	path('forums/<int:pk>/removeDislike', login_required(ForumRemoveDislike.as_view()), name="forum-removedislike"),
	path('forums/<int:pk>/view', ForumView.as_view(), name="forum-view"),
	path('threads/api/delete_thread', ThreadDeleteView.as_view(), name="thread_delete"),
	path('threads/api/delete_comment', ThreadCommentDeleteView.as_view(), name="thread_comment_delete"),
	path('youtube_token', views.youtube_token_v, name='get_youtube_token'),	
	path('profile', login_required(views.update_profile), name="profile"),
	path('experiences', ExperiencesView.as_view(), name="experiences"),
	path('contact-us', ContactUsView.as_view(), name="contact-us"),
	path('about-us', AboutUsView.as_view(), name="about-us"),
	path('send_email', views.ContactUsSendEmail, name="contact_us_send_email"),
	path('document', DocumentView.as_view(), name="document"),
	path('experiences/manage', ManageExperiencesView.as_view(), name="experiences_manage"),
	path('experiences/modify', ModifyExperienceStatus.as_view(), name="experiences_modify"),
	path('experiences/api/pendingexperiences', PendingExperiences.as_view(), name="experiences_pending"),
	path('experiences/api/delete_experience', DeleteExperienceView.as_view(), name="delete_experience"),
	path('experiences/create', CreateExperience.as_view(), name="experiences_create"),
	path('experiences/<int:pk>/', ExperienceDetailView.as_view(), name="experience-detail"),
	path('experiences/<str:order>', ExperiencesOrdered.as_view(), name="experiences-ordered"),
	path('experiences/<int:pk>/like', login_required(ExperienceLike.as_view()), name="experience-like"),
	path('experiences/<int:pk>/dislike', login_required(ExperienceDislike.as_view()), name="experience-dislike"),
	path('experiences/<int:pk>/removeLike', login_required(ExperienceRemoveLike.as_view()), name="experience-removelike"),
	path('experiences/<int:pk>/removeDislike', login_required(ExperienceRemoveDislike.as_view()), name="experience-removedislike"),
	path('myforums/', login_required(MyForumsView.as_view()), name="my-forums"),
	path('myexperiences/', login_required(MyExperiencesView.as_view()), name="my-experiences"),
	path('experiences/<int:pk>/view', ExperienceView.as_view(), name="experience-view"),
	path('mycomments/', login_required(MyCommentsView.as_view()), name="my-comments"),
	path('box', login_required(BoxView.as_view()), name="box"),
	path('guide_general/<int:pk>', login_required(GuideView.as_view()), name="guides"),
	path('crossword', CrossWordView.as_view(), name="crossword"),
	path('search', SearchView.as_view(), name="search"),
	path('guides/addAnswer', AddAnswerView.as_view(), name="add_answer"),
	path('guides/addReview', AddToolboxReview.as_view(), name="add_review"),
	path('guides/manage', ManageToolboxesView.as_view(), name="toolboxes_manage"),
	path('guides/comment/<str:user_id>/<str:tb_id>', CommentToolboxView.as_view(), name="toolbox_comment"),
	path('guides/view_comment/<str:tb_id>', ViewToolboxCommentView.as_view(), name="view_toolbox_comment"),
	path('toolbox/api/comment', ToolboxAddCommentApiView.as_view(), name="addtbxcomment")
]