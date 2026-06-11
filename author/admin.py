from django.contrib import admin
from author.models import Author
from book.models import Book

class BookInLine(admin.TabularInline):
    model = Book
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name']
    list_filter = ['full_name']
    search_fields = ['full_name']

    inlines = [BookInLine]
