from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    image = models.URLField()

    def __str__(self):
        return self.name
