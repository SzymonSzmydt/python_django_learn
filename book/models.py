from django.db import models
from author.models import Author
from genre.models import Genre

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publication_date = models.DateField()
    cover = models.URLField(max_length=100)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')


    def __str__(self):
        return self.title
