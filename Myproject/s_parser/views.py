from django.shortcuts import get_object_or_404, render
from .models import AllLanguages
from django.http import HttpResponse


def index(request):
    return render(request, 's_parser/index.html')


def detail(request, languageName):
    language = get_object_or_404(language, pk=languageName)
    return render(request, 's_parser/detail.html', {'language': language})