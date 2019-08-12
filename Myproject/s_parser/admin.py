from django.contrib import admin

# Register your models here.
from .models import AllLanguages
admin.site.register(AllLanguages)

from .models import BlogData
admin.site.register(BlogData)