from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from categories.models import Category
from platforms.models import Platform


class Game(models.Model):
    class PEGI(models.IntegerChoices):
        PEGI3 = 3, 'Pegi3'
        PEGI7 = 7, 'Pegi7'
        PEGI12 = 12, 'Pegi12'
        PEGI16 = 16, 'Pegi16'
        PEGI18 = 18, 'Pegi18'

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(blank=True, upload_to='covers/', default='covers/default.jpg')
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    released_at = models.DateField()
    pegi = models.IntegerField(choices=PEGI.choices)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    platforms = models.ManyToManyField(Platform, blank=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)
