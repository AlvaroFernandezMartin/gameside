from colorfield.fields import ColorField
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    color = ColorField(blank=True)

    def __str__(self):
        return f' Pk: {self.pk},Name: {self.name}, Slug: {self.slug}, Description: {self.description}, Color: {self.color} '
