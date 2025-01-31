from django.db import models
from games.models import Game
from django.conf import settings
import uuid
# Create your models here.
class Order(models.Model):
    class Status(models.IntegerChoices) :
        INITIATED = 1, 'Initiated'
        CONFIRMED = 2, 'Confirmed'
        CANCELLED = 3, 'Paid'
        PAID = -1, 'Cancelled'
    status = models.IntegerField(choices=Status.choices , default=Status.INITIATED) 
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    games = models.ManyToManyField(Game)