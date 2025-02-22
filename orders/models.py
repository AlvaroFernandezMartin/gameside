import uuid

from django.conf import settings
from django.db import models

from games.models import Game


# Create your models here.
class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1, 'Initiated'
        CONFIRMED = 2, 'Confirmed'
        PAID = 3, 'Paid'
        CANCELLED = -1, 'Cancelled'

    status = models.IntegerField(choices=Status.choices, default=Status.INITIATED)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)

    @property
    def price(self):
        return sum(game.price for game in self.games.all())  


    def status_order(self):
        if self.status == 3:
            return self.key
        else:
            return None 
    def __str__(self):
        return f'Key:{self.key}, Status: {self.status}, User: {self.user}, Games: {self.games} '
