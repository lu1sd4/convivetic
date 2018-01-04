from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView

class Index(TemplateView):
	#context = {}
	#return render(request, 'app/index.html', context)
	template_name = 'app/index.html' 