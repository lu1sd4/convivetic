from django.urls import path

from .views import Index
from .views import Login

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('login', Login.as_view(), name='login')
]