from django.contrib import admin
from genre.models import Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']