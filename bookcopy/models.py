from django.db import models
from book.models import Book

class BookCopy(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = 'dostępny', 'Dostępny'
        BORROWED = 'wypożyczony', 'Wypożyczony'
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='bookcopys')

    def __str__(self):
        return self.status