from django.urls import path

from . import views

urlpatterns = [
    # main /s_parser/
    path('', views.index, name='index'),
    # /s_parser/java/
    #path('<cha:languageName>/', views.detail, name='detail'),
]
