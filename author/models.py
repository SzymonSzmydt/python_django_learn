from django.db import models
from sqlalchemy import Null

class Author(models.Model):
    full_name = models.CharField(max_length=200)
    image = models.CharField(max_length=100, default=Null)

    def __str__(self):
        return self.full_name