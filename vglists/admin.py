from django.contrib import admin

# Register your models here.

from .models import VideogameList, Videogame

admin.site.register(VideogameList)
admin.site.register(Videogame)
