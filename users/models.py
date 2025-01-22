from django.db import models
from django.conf import settings
# Create your models here.

class Token(models.Model):
    user = models.OneToOneField( settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    key = models.UUIDField(unique=True)
    created_at = models.DateTimeField(auto_now_add=False)