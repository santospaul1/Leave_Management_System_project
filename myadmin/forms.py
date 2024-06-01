from myadmin.models import Admin
from django import forms


class AdminForm:
    class meta:
        model = Admin
        fields = ['fullname', 'email', 'password', 'username']