
from django import forms

from employee.models import Employee


class EmployeeUpdateForm(forms.ModelForm):

  class Meta:
    model = Employee
    fields = ['firstName', 'lastName', 'gender', 'mobileno',
              'address', 'city', 'country', 'department', 'status']

EMP_CHOICES = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive'),
)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'empcode',
            'firstName',
            'lastName',
            'email',
            'password',
            'images',
            'gender',
            'department',
            'address',
            'city',
            'country',
            'mobileno',
            'status',
        ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['images','firstName', 'lastName','gender', 'address', 'city', 'country', 'mobileno']

