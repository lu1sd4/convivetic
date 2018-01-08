from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import UserProfile

class LoginForm(AuthenticationForm):
	username = forms.CharField(
		max_length=20,
		label = 'Nombre de usuario'
	)
	password = forms.CharField(
		label= 'Contraseña',
		widget=forms.PasswordInput
	)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name', 'email']
		labels = {
			'username' : 'Nombre de usuario',
			'password' : 'Contraseña',
			'first_name' : 'Nombres',
			'last_name' : 'Apellidos',
			'email' : 'Correo electrónico'
		}

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
			'phone_number' : 'Número de teléfono',
			'bio' : 'Más información sobre usted',
			'is_conflict_participant' : '¿Es usted participe del conflicto armado?',
			'is_conflict_victim' : '¿Es usted víctima del conflicto armado?',
			'is_living_in_conflict_zone' : '¿Es usted habitante de una zona de conflicto?'
		}
		widgets = {
			'is_conflict_participant' : forms.RadioSelect,
			'is_conflict_victim' : forms.RadioSelect,
			'is_living_in_conflict_zone' : 	forms.RadioSelect
		}