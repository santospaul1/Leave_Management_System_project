from django.db import models
from django.contrib.auth.models import User

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    CreationDate = models.DateField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # Delete the associated user
        self.user.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.username


# Create your models here.
