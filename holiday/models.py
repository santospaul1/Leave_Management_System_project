from django.db import models

# Create your models here.

class Holiday(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(unique=True)

    def __str__(self):
        return self.name
