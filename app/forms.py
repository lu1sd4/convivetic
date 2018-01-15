from django import forms

from datetime import datetime

from django.contrib.auth.models import User, Group
from django.contrib.auth import forms as auth_forms

from .models import *

class LoginForm(auth_forms.AuthenticationForm):
	username = forms.CharField(
		max_length=20,
		label = 'Nombre de usuario'
	)
	password = forms.CharField(
		label= 'Contraseña',
		widget=forms.PasswordInput
	)

class UserForm(auth_forms.UserCreationForm):
	group = forms.ModelChoiceField(queryset=Group.objects.all(),
								   required=True,
								   empty_label='¿Qué tipo de usuario eres?')
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'group']
		labels = {
			'username' : 'Nombre de usuario',
			'password1' : 'Contraseña',
			'password2' : 'Confirmar contraseña',
			'first_name' : 'Nombres',
			'last_name' : 'Apellidos',
			'email' : 'Correo electrónico'
		}
		widgets = {
			'password1' : forms.PasswordInput,
			'password2' : forms.PasswordInput,
			'email' : forms.EmailInput
		}

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['password1'].min_length = 8
		self.fields['password1'].label = 'Contraseña'
		self.fields['password2'].min_length = 8
		self.fields['password2'].label = 'Confirmar contraseña'

class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['title', 'birth_date', 'gender', 'nationality', 'country_of_residence', 'phone_number', 'bio', 'is_conflict_participant', 'is_conflict_victim', 'is_living_in_conflict_zone']
		labels = {
			'title' : 'Título',
			'birth_date' : 'Fecha de nacimiento',
			'gender' : 'Género',
			'nationality' : 'Nacionalidad',
			'country_of_residence' : 'País de residencia',
			'phone_number' : 'Teléfono',
			'bio' : 'Más información sobre usted',
			'is_conflict_participant' : '¿Es usted participe del conflicto armado?',
			'is_conflict_victim' : '¿Es usted víctima del conflicto armado?',
			'is_living_in_conflict_zone' : '¿Es usted habitante de una zona de conflicto?'
		}
		widgets = {
			'is_conflict_participant' : forms.RadioSelect,
			'is_conflict_victim' : forms.RadioSelect,
			'is_living_in_conflict_zone' : 	forms.RadioSelect,
			'birth_date' : forms.DateInput(attrs={'type':'date','max':datetime.now().date()}, format='%Y-%m-%d')
		}

class ThreadForm(forms.ModelForm):
	class Meta:
		model = Thread
		fields = ['title', 'description', 'video_url', 'audio_url', 'img']
		labels = {
			'title' : 'Título de la discusión',
			'description' : 'Cuerpo de texto de la discusión'			
		}
		widgets = {
			'title' : forms.Textarea,
			'description' : forms.Textarea,
			'video_url' : forms.HiddenInput,
			'audio_url' : forms.HiddenInput
		}