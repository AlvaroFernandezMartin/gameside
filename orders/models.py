from django.db import models
from games.models import Game
from django.conf import settings

# Create your models here.
class Order(models.Model):
    class Status(models.IntegerChoices) :
        INITIATED = 0
        CONFIRMED = 1
        CANCELLED = 2
        PAID = 3
    status = models.IntegerField(choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)
    key = models.UUIDField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)