from django.db import models
from colorfield.fields import ColorField

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    color = ColorField(blank=True)
