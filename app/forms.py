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

class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['title', 'birth_date', 'gender', 'nationality', 'country_of_residence', 'phone_number', 'bio', 'is_conflict_participant', 'is_conflict_victim', 'is_living_in_conflict_zone']