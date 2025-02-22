# Generated by Django 5.1.5 on 2025-02-10 15:45

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('color', colorfield.fields.ColorField(blank=True, default='#ffffff', image_field=None, max_length=25, samples=None)),
            ],
        ),
    ]
