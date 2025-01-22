from django.db import models

class Platform(models.Model):
    name = models.CharField(max_length=100)  
    slug = models.SlugField(unique=True)  
    description = models.TextField(blank=True)  
    logo = models.ImageField(upload_to='platform_logos/') 

    def __str__(self):
        return self.name
