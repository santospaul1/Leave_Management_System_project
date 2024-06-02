from django import forms
from department.models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'department_shortname', 'department_code']