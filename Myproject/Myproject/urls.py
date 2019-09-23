from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('Myapp.urls', namespace="Myapp")),
    path('s_parser/', include('s_parser.urls')),
    path('admin/', admin.site.urls),
]