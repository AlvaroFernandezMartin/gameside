from django.db import models
from categories.models import Category
from platforms.models import Platform
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Game(models.Model):
    class PEGI(models.IntegerChoices):
        PEGI3 = 3, 'PEGI 3'
        PEGI7 = 7, 'PEGI 7'
        PEGI12 = 12, 'PEGI 12'
        PEGI16 = 16, 'PEGI 16'
        PEGI18 = 18, 'PEGI 18'

    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to='covers/', default='default_cover.png')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()
    released_at = models.DateField()
    pegi = models.IntegerField(choices=PEGI.choices)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    platforms = models.ManyToManyField(Platform, blank=True)

    def __str__(self):
        return self.title

    


class Review(models.Model):
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment =  models.TextField()
    game = models.ForeignKey(Game,on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)