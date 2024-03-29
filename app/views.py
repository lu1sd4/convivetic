from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import JsonResponse
from django.template import loader
from django.db.models import Count

from django.urls import reverse

from django.views.generic import TemplateView
from django.views.generic import FormView
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic import DetailView

from django.views.generic.detail import SingleObjectMixin

from django.views.generic.edit import CreateView
from django.views.generic.edit import FormMixin

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.models import User
from django.contrib import messages

# Email verification

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage, BadHeaderError

# Youtube Token Retrieval

from .tokens import youtube_token

from django.db import transaction
from .forms import *

from .models import *

from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from django.contrib.auth.mixins import UserPassesTestMixin

from django.http import JsonResponse

import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import Http404



def handler404(request, exception, template_name='app/404.html'):
    return render(request, template_name, status=404)

def handler403(request, exception, template_name='app/403.html'):
    return render(request, template_name, status=403)

class Index(ListView):
	template_name = 'app/index.html'
	context_object_name = 'thread_list'
	queryset = Thread.objects.order_by('pub_date')[:4]

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['secondary_threads'] = Thread.objects.annotate(likes=Count('like')).order_by('pub_date')[4:8]
		context['experiences'] = Experience.objects.filter(status='A').order_by('pub_date')[:9]
		context['th_quantity'] = Thread.objects.all().count()
		group =  Group.objects.get(name="Administrador")
		if group in self.request.user.groups.all():
			pending_experiences = Experience.objects.filter(status='P').count()
			if pending_experiences > 0:
				messages.info(self.request, "Tienes "+str(pending_experiences)+" Experiencia(s) pendientes por revisar.")
		return context


class Login(LoginView):
	template_name = 'app/login.html'
	authentication_form = LoginForm
	redirect_authenticated_user = True

class UsernameCheck(View):
	def get(self, request, *args, **kwargs):
		username = self.kwargs['user_id']
		if username_present(username):
			return HttpResponse()
		return HttpResponseBadRequest()

def username_present(username):
	if User.objects.filter(username=username).exists():
		return True
	return False

class Forums(FormView):
	template_name = 'app/forums.html'
	model = Thread
	form_class = ThreadForm
	success_url = '/forums'    

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		page = self.request.GET.get('page', 1)

		try:
			order = self.kwargs['order']
		except KeyError:
			order = 'new'
		context['order'] = order		
		if order == 'new':
			thread_list = Thread.objects.all().order_by('-pub_date')
		elif order == 'popular':
			thread_list = Thread.objects.all().annotate(likes=Count('comment')).order_by('-likes')
			
		paginator = Paginator(thread_list, 8)
			    
		try:
			threads = paginator.page(page)
		except PageNotAnInteger:
			threads = paginator.page(1)
		except EmptyPage:
			threads = paginator.page(paginator.num_pages)
		context['thread_list'] = threads

		return context

	def post(self, request, *args, **kwargs):		
		form = self.get_form()
		if form.is_valid():
			thread = form.save(commit=False)
			thread.author = request.user
			thread.save()
			tags_raw = form.cleaned_data['tags']
			tags_array = [x.strip() for x in tags_raw.split(',')]
			for tag_name in tags_array:
				tag = ThreadTag.objects.filter(name = tag_name)
				if not tag:
					tag = ThreadTag.objects.create(name = tag_name)
				else:
					tag = tag[0]
				thread.tags.add(tag)
			thread.save()
			messages.success(request, 'Tu discusión se ha publicado con éxito.')
			return redirect('thread-detail', pk=thread.id)
		else:
			return self.form_invalid(form)

class ForumsOrdered(ListView):
	template_name = 'app/forums.html'
	paginate_by = 8

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['order'] = self.kwargs['order']
		return context

	def get_queryset(self):
		criterium = self.kwargs['order']
		if(criterium == 'popular' or criterium == 'new'):
			return self.get_query_criterium(criterium)
		else:
			return Experience.objects.none()


	def get_query_criterium(self, criterium):

		
		return {
			'popular': Thread.objects.order_by('-title'),
			'new': Thread.objects.order_by('-pub_date'),
		}[criterium]


class ForumDetail(FormMixin, DetailView):
	model = Thread
	template_name = 'app/thread_detail.html'
	form_class = ThreadCommentForm

	def get_success_url(self):
		return reverse('thread-detail', kwargs={'pk':self.object.id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		thread_pk = self.kwargs['pk']
		context['thread_pk'] = thread_pk

		like = Like.objects.filter(thread = thread_pk, author = self.request.user.id).count()
		dislike = Dislike.objects.filter(thread = thread_pk, author = self.request.user.id).count()

		status = 'no_like'
		if like > 0:
			status = 'like'
		elif dislike > 0:
			status = 'dislike'

		context['like_status'] = status

		context['form'] = ThreadCommentForm(instance=Comment(
				thread=self.object
			)
		)

		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			messages.success(request, 'Comentario publicado con éxito')
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		comment = form.save(commit=False)
		comment.author = self.request.user
		comment.save()
		return super(ForumDetail, self).form_valid(form)



class ForumLike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk=forum_id)
		author = request.user
		like = Like(thread = forum, author = author)
		like.save()
		likes_c = Like.objects.filter(thread = forum_id).count()
		dislikes_c = Dislike.objects.filter(thread = forum_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ForumRemoveLike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk=forum_id)
		author = request.user
		like = Like.objects.filter(thread = forum_id, author = author.id)
		like.delete()
		likes_c = Like.objects.filter(thread = forum_id).count()
		dislikes_c = Dislike.objects.filter(thread = forum_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ForumDislike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk=forum_id)
		author = request.user
		dislike = Dislike(thread = forum, author = author)
		dislike.save()
		likes_c = Like.objects.filter(thread = forum_id).count()
		dislikes_c = Dislike.objects.filter(thread = forum_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ForumRemoveDislike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk=forum_id)
		author = request.user
		dislike = Dislike.objects.filter(thread = forum_id, author = author.id)
		dislike.delete()
		likes_c = Like.objects.filter(thread = forum_id).count()
		dislikes_c = Dislike.objects.filter(thread = forum_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ForumView(View):
	def get(self, request, *args, **kwargs):
		forum_id = self.kwargs['pk']
		forum = get_object_or_404(Thread, pk = forum_id)
		forum.views = forum.views + 1
		forum.save()
		return HttpResponse(forum.views)

class ForumComment(View):
	
	def get(self,request, *args, **kwargs):
		forum_id = self.kwargs['pk']
		comment_content = self.kwargs['content']
		forum = get_object_or_404(Thread, pk = forum_id)
		author = request.user
		#comment = Comment(thread=forum, author=author, content=comment_content, )
		return HttpResponse()

@transaction.atomic
def register_user(request):
	if request.method == "POST":
		user_form = UserForm(request.POST, prefix="user")
		profile_form = ProfileForm(request.POST, prefix="profile")
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save(commit=False)			
			user.is_active = False
			user.save()
			user.groups.clear()
			user.groups.add(user_form.cleaned_data['group'])
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.save()
			current_site = get_current_site(request)
			mail_subject = 'Activa tu cuenta de ConviveTIC'
			message = render_to_string('app/acc_activation_email.html', {
				'user' : user,
				'domain' : current_site.domain,
				'uid' : force_text(urlsafe_base64_encode(force_bytes(user.pk))),
				'token': account_activation_token.make_token(user)
			})
			to_email = user_form.cleaned_data.get('email')
			email = EmailMessage(
				mail_subject, message, to=[to_email]
			)
			email.send()
			messages.success(request, 'Te has registrado. Recibirás un correo electrónico con instrucciones para completar la activación de tu cuenta.')
			return redirect('/')
	else:
		user_form = UserForm(prefix="user", initial={'group' : 1})
		profile_form = ProfileForm(prefix="profile")
	context = {
		"user_form": user_form,
		"profile_form": profile_form
	}
	return render(request, 'app/signup.html', context)

@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.groups.clear()
            user.groups.add(user_form.cleaned_data['group'])
            user.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado!')
            return render(request, 'app/profile.html', { 
            	'user_form': user_form,
        		'profile_form': profile_form
            })
        else:
            messages.error(request, 'El formulario no es válido.')
    else:
        user_form = UserUpdateForm(instance=request.user, initial={'group' : request.user.groups.get().pk})
        profile_form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'app/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Gracias por confirmar tu correo. Ahora puedes iniciar sesión.')
        return redirect('/')
    else:
        return HttpResponse('Tu enlace de activación no es válido.')

class PasswordReset(PasswordResetView):
	template_name = 'app/password_reset_request.html'
	email_template_name = 'app/password_reset_email.html'
	subject_template_name = 'app/password_reset_subject.txt'

class PasswordResetDone(PasswordResetDoneView):
	template_name = 'app/password_reset_request_done.html'	

class PasswordResetConfirm(PasswordResetConfirmView):
	template_name = 'app/password_reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
	template_name = 'app/password_reset_complete.html'

@csrf_exempt
def youtube_token_v(request):
	data = { 
		'token' : youtube_token.get_youtube_token(),
		'apiKey' : settings.API_KEY,
		'folderId' : settings.DRIVE_FOLDER_ID
	}
	return(JsonResponse(data))

class YoutubeUploadTest(TemplateView):
	template_name = 'app/test_youtube.html'

class DriveUploadTest(TemplateView):
	template_name = 'app/test_drive.html'

class CreateExperience(LoginRequiredMixin, FormView):
	template_name = 'app/create_experience.html'
	model = Experience
	form_class = ExperienceForm
	success_url = '/myexperiences'

	def post(self, request, *args, **kwargs):		
		form = self.get_form()
		if form.is_valid():
			exp = form.save(commit=False)
			exp.author = request.user
			exp.save()
			tags_raw = form.cleaned_data['tags']
			tags_array = [x.strip() for x in tags_raw.split(',')]
			for tag_name in tags_array:
				tag = ExperienceTag.objects.filter(name = tag_name)
				if not tag:
					tag = ExperienceTag.objects.create(name = tag_name)
				else:
					tag = tag[0]
				exp.tags.add(tag)
			exp.save()
			messages.success(request, 'Tu experiencia se ha enviado con éxito. Está pendiente de aprobación para ser publicada.')
			return redirect('experience-detail', pk=exp.id)
		else:
			return self.form_invalid(form)			



class AboutUsView(TemplateView):
	template_name= "app/about_us.html"

class ContactUsView(TemplateView):
	template_name = "app/contact_us.html"

class DocumentView(TemplateView):
	template_name = "app/document.html"

@csrf_exempt
def ContactUsSendEmail(request):
	if request.method =="POST":
		name = request.POST.get('name', '')
		lastname = request.POST.get('lastname', '')
		email = request.POST.get('email', '')
		comment = request.POST.get('comment', '')
		comment = 'Correo: ' + email + '\nNombre: ' + name + ' ' + lastname + '\n\n' + 'Mensaje:\n' + comment
		phone = request.POST.get('phone', '')
		data={}
		try:
			message = EmailMessage(subject='Nuevo mensaje en la página', body=comment, from_email=email, to=[settings.EMAIL_HOST_USER])
			message.send()
			data["type"] = "Success",
			data["message"] = "¡ Envio exitoso !"
		except BadHeaderError:
			data["type"] = "error"
			data["message"] = "Datos invalidos, por favor verifica la información."
	return (JsonResponse(data))


class ExperienceDetailView(DetailView):
	model = Experience
	template_name = 'app/experience_detail.html'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		experience_pk = self.kwargs['pk']
		context['experience_pk'] = experience_pk

		like = ExperiencesLike.objects.filter(experience = experience_pk, author = self.request.user.id).count()
		dislike = ExperiencesDislike.objects.filter(experience = experience_pk, author = self.request.user.id).count()

		status = 'no_like'
		if like > 0:
			status = 'like'
		elif dislike > 0:
			status = 'dislike'

		context['like_status'] = status

		return context


class ExperienceLike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		exp_id = self.kwargs['pk']
		exp = get_object_or_404(Experience, pk=exp_id)
		author = request.user
		like = ExperiencesLike(experience = exp, author = author)
		like.save()
		likes_c = ExperiencesLike.objects.filter(experience = exp_id).count()
		dislikes_c = ExperiencesDislike.objects.filter(experience = exp_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ExperienceRemoveLike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		exp_id = self.kwargs['pk']
		exp = get_object_or_404(Experience, pk=exp_id)
		author = request.user
		like = ExperiencesLike.objects.filter(experience = exp_id, author = author.id)
		like.delete()
		likes_c = ExperiencesLike.objects.filter(experience = exp_id).count()
		dislikes_c = ExperiencesDislike.objects.filter(experience = exp_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ExperienceDislike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		exp_id = self.kwargs['pk']
		exp = get_object_or_404(Experience, pk=exp_id)
		author = request.user
		dislike = ExperiencesDislike(experience = exp, author = author)
		dislike.save()
		likes_c = ExperiencesLike.objects.filter(experience = exp_id).count()
		dislikes_c = ExperiencesDislike.objects.filter(experience = exp_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ExperienceRemoveDislike(LoginRequiredMixin, View):
	login_url = '/login'

	def get(self, request, *args, **kwargs):

		exp_id = self.kwargs['pk']
		exp = get_object_or_404(Experience, pk=exp_id)
		author = request.user
		dislike = ExperiencesDislike.objects.filter(experience = exp_id, author = author.id)
		dislike.delete()
		likes_c = ExperiencesLike.objects.filter(experience = exp_id).count()
		dislikes_c = ExperiencesDislike.objects.filter(experience = exp_id).count()
		data = {
			'likes' : likes_c,
			'dislikes' : dislikes_c
		}

		return JsonResponse(data)

class ExperiencesView(ListView):
	template_name = 'app/experiences.html'
	context_object_name = 'experiences'
	queryset = Experience.objects.order_by('pub_date').filter(status='A')
	paginate_by = 8

	def get_context_data(self, **kwargs):
		context = super(ExperiencesView, self).get_context_data(**kwargs)
		context['order'] = 'new'
		return context;

class ExperiencesOrdered(ListView):
	template_name = 'app/experiences.html'
	context_object_name = 'experiences'
	paginate_by = 8

	def get_context_data(self, **kwargs):
		context = super(ExperiencesOrdered, self).get_context_data(**kwargs)
		context['order'] = self.kwargs['order']
		return context;

	def get_queryset(self):
		criterium = self.kwargs['order']
		if(criterium == 'popular' or criterium == 'new'):
			return self.get_query_criterium(criterium).filter(status='A')
		else:
			return Experience.objects.none()

	def get_query_criterium(self, criterium):
		return {
			'popular': Experience.objects.order_by('-title'),
			'new': Experience.objects.order_by('-pub_date'),
		}[criterium]

class ExperienceView(View):
	def get(self, request, *args, **kwargs):
		experience_id = self.kwargs['pk']
		experience = get_object_or_404(Experience, pk = experience_id)
		experience.views = experience.views + 1
		experience.save()
		return HttpResponse(experience.views)

class MyForumsView(ListView):
	template_name = 'app/my_forums.html'
	context_object_name = 'user_threads'
	paginate_by = 8

	def get_queryset(self):
		user_id = self.request.user.id
		return Thread.objects.filter(author = user_id)

class MyExperiencesView(ListView):
	template_name = 'app/my_experiences.html'
	context_object_name = 'user_experiences'
	paginate_by = 6

	def get_queryset(self):
		user_id = self.request.user.id
		return Experience.objects.filter(author = user_id)

class MyCommentsView(ListView):
	template_name = 'app/my_comments.html'
	paginate_by = 8
	context_object_name = 'my_comments'

	def get_queryset(self):
		user_id = self.request.user.id
		return Comment.objects.filter(author = user_id)

class UserIsAdminMixin(UserPassesTestMixin):
	raise_exception = True
	def test_func(self):
		group =  Group.objects.get(name="Administrador")
		return group in self.request.user.groups.all()

class PendingExperiences(UserIsAdminMixin, View):
	def get(self, request, *args, **kwargs):
		data = {
			'count': Experience.objects.filter(status='P').count()
		}
		return JsonResponse(data)

class ManageExperiencesView(UserIsAdminMixin, TemplateView):
	template_name = "app/manage_experiences.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pending_experiences = Experience.objects.filter(status='P')
		context['pending_experiences'] = pending_experiences 
		approved_experiences = Experience.objects.filter(status='A')
		context['approved_experiences'] = approved_experiences
		rejected_experiences = Experience.objects.filter(status='R')
		context['rejected_experiences'] = rejected_experiences
		return context

class ModifyExperienceStatus(UserIsAdminMixin, View):
	def post(self, request, *args, **kwargs):
		try:
			data = json.loads(request.body)
			exp = Experience.objects.get(pk=data['pk'])
			if data['action'] == 'A':
				messages.success(request, 'Experiencia aprobada para publicación')
				exp.status = 'A'
			elif data['action'] == 'R':
				messages.error(request, 'Experiencia no aprobada para publicación')
				exp.status = 'R'
			exp.save()
			return HttpResponse()
		except Experience.DoesNotExist:
			return HttpResponseBadRequest()

class DeleteExperienceView(LoginRequiredMixin, View):
	raise_exception = True
	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)		
		try:
			exp = Experience.objects.get(pk=data['pk'])
			if exp.author == request.user:
				exp.delete()
				return HttpResponse()
			else:
				return JsonResponse(status=403, data={'error':True, 'message':'No eres el autor de la experiencia'})	
		except Experience.DoesNotExist:
			return JsonResponse(status=403, data={'error':True, 'message':'La experiencia no existe'})

class ThreadDeleteView(LoginRequiredMixin, View):
	raise_exception = True
	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)		
		try:
			thr = Thread.objects.get(pk=data['pk'])
			if thr.author == request.user:
				thr.delete()
				return HttpResponse()
			else:
				return JsonResponse(status=403, data={'error':True, 'message':'No eres el autor de la discusión'})	
		except Experience.DoesNotExist:
			return JsonResponse(status=403, data={'error':True, 'message':'La discusión no existe'})

class ThreadCommentDeleteView(LoginRequiredMixin, View):
	raise_exception = True
	def post(self, request, *args, **kwargs):
		data = json.loads(request.body)		
		try:
			comm = Comment.objects.get(pk=data['pk'])
			if comm.author == request.user:
				comm.delete()
				return HttpResponse()
			else:
				return JsonResponse(status=403, data={'error':True, 'message':'No eres el autor del comentario'})	
		except Experience.DoesNotExist:
			return JsonResponse(status=403, data={'error':True, 'message':'El comentario no existe'})

class BoxView(TemplateView):
	template_name='app/box.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		current_user = self.request.user
		solved_by_user = ToolboxUser.objects.filter(user=current_user).values('toolbox')
		unsolved_toolboxes = Toolbox.objects.exclude(id__in=solved_by_user)
		solved_toolboxes = Toolbox.objects.filter(id__in=solved_by_user)
		context['unsolved'] = unsolved_toolboxes
		context['solved'] = solved_toolboxes
		return context


class GuideView(TemplateView):
	template_name = 'app/guide_general.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pk = self.kwargs["pk"]
		toolbox = list(Toolbox.objects.filter(guide_n=pk))
		questions = list(Question.objects.filter(toolbox=pk).order_by('order'))
		if(len(toolbox) != 0 and len(questions) != 0):
			context["toolbox"] = serializers.serialize("json", toolbox + questions)
		else:
			raise Http404

		return context

class CrossWordView(TemplateView):
	template_name = 'app/crossword.html'

class SearchView(TemplateView):
	template_name = 'app/search.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		q = self.request.GET.get('q')
		context['q'] = q
		context['threads'] = Thread.objects.filter(description__contains=q).annotate(thlikes=Count('like')).order_by('-thlikes')[0:10]
		context['experiences'] = Experience.objects.filter(content__contains=q, status='A').annotate(xplikes=Count('experienceslike')).order_by('-xplikes')[0:10]
		return context

class AddAnswerView(View):
	def post(self, request, *args, **kwargs):
		question_id = request.POST.get("id")
		question = Question.objects.get(pk=question_id)
		usr = self.request.user
		answer = request.POST.get("answer")
		Answer.objects.create(question = question, user = usr, answer = answer)
		return HttpResponse(status=200)

class AddToolboxReview(View):
	def post(self, request, *args, **kwargs):
		toolbox_id = request.POST.get("toolbox")
		toolbox = Toolbox.objects.get(pk=toolbox_id)
		usr = self.request.user
		ToolboxUser.objects.create(toolbox = toolbox, user = usr)
		return HttpResponse(status=200)

class ManageToolboxesView(UserIsAdminMixin, TemplateView):
	template_name = "app/manage_toolboxes.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pending_toolboxes = ToolboxUser.objects.filter(comment__exact='')
		context['pending_toolboxes'] = pending_toolboxes
		commented_toolboxes = ToolboxUser.objects.exclude(comment__exact='')
		context['commented_toolboxes'] = commented_toolboxes
		return context


class CommentToolboxView(UserIsAdminMixin, TemplateView):
	template_name = "app/comment_toolbox.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['option_letters'] = { 0: 'A', 1: 'B', 2: 'C', 3: 'D' }

		user_id = kwargs['user_id']
		user = User.objects.get(id=user_id)

		tb_id = kwargs['tb_id']
		toolbox = Toolbox.objects.get(id=tb_id)
		
		context['toolbox'] = toolbox
		context['user'] = user
		
		questions = toolbox.question_set.exclude(q_type__exact='TEMP_INTRO').exclude(q_type__exact='TEMP_TEXT').order_by('order')		
		context['questions'] = questions
		
		answers = user.answer_set.filter(question__in=questions).order_by('question__order')
		context['answers'] = answers

		return context

class ToolboxAddCommentApiView(UserIsAdminMixin, View):
	def post(self, request, *args, **kwargs):	
		data = json.loads(request.body)
		toolbox_id = data.get("toolbox_id")
		toolbox = Toolbox.objects.get(pk=toolbox_id)
		user_id = data.get("user_id")
		user = User.objects.get(pk=user_id)
		tbUsr = ToolboxUser.objects.get(toolbox = toolbox, user = user)
		tbUsr.comment = data.get("comment")
		tbUsr.save()
		return HttpResponse(status=200)

class ViewToolboxCommentView(LoginRequiredMixin, TemplateView):
	template_name = "app/view_toolbox_comment.html"
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		context['option_letters'] = { 0: 'A', 1: 'B', 2: 'C', 3: 'D' }

		user = self.request.user

		tb_id = kwargs['tb_id']
		toolbox = Toolbox.objects.get(id=tb_id)
		
		context['toolbox'] = toolbox
		context['user'] = user
		
		questions = toolbox.question_set.exclude(q_type__exact='TEMP_INTRO').exclude(q_type__exact='TEMP_TEXT').exclude(q_type__exact='TEMP_FILL_THE_BLANKS').order_by('order')		
		context['questions'] = questions
		
		answers = user.answer_set.filter(question__in=questions).order_by('question__order')
		context['answers'] = answers

		tbUsr = ToolboxUser.objects.get(toolbox = toolbox, user = user)
		context['comment'] = tbUsr.comment

		return context