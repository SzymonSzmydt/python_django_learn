from django.db import models
from bookcopy.models import BookCopy
from django.contrib.auth.models import User


class Reservation(models.Model):
    reservation_date = models.DateField()
    expiration_date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    bookcopy = models.ForeignKey(BookCopy, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return f"{self.user} - {self.bookcopy} ({self.reservation_date})"