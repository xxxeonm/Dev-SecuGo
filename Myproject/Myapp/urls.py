from . import views
from django.urls import path
app_name="Myapp"
urlpatterns = [
    path('', views.index, name="index"),
    path('learn', views.learn ,name="learn"),
    path('compare', views.compare,name="compare"),
]