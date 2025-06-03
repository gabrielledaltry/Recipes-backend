from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image = models.URLField()
    saved_by = models.ManyToManyField(User, related_name='saved_recipes', blank=True)

    def __str__(self):
        return self.name
