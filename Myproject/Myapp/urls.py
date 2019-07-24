from . import views
from django.urls import path
app_name="Myapp"
urlpatterns = [
    path('', views.index, name="index"),
    path('pro', views.pro ,name="pro"),
    path('compare', views.compare,name="compare"),


]