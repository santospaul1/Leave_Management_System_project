from django.db import models

# Create your models here.

class Department(models.Model):

    department_name = models.CharField(max_length=255)
    department_shortname = models.CharField(max_length=50)
    department_code = models.CharField(max_length=10)
    CreationDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.department_name
