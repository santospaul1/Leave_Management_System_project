from django.db import models
from django.contrib.auth.models import User

from department.models import Department

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)
EMP_CHOICES = (
        ( 'Active', 'Active'),
        ( 'Inactive', 'Inactive'),
        )
UN_CHOICES = (
    ('Union', 'Union'),
    ('Non-Union', 'Non-Union'),
    ('Others', 'Others')

)

class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    empcode = models.CharField(max_length=10, primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    images = models.ImageField(upload_to='images/', null=True)
    employee_type = models.CharField(
        max_length=10,
        choices=UN_CHOICES,
        default='Non-Union'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='Male'
    )
    dob = models.DateField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default="80100")
    city = models.CharField(max_length=100, default="Mombasa")
    country = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=10)
    status = models.CharField(
        max_length=10,
        choices=EMP_CHOICES,
        default='Active'
    )
    CreationDate = models.DateField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # Delete the associated user
        self.user.delete()
        super().delete(*args, **kwargs)
    def __str__(self):
        return f"{self.empcode} - {self.firstName} {self.lastName}"



