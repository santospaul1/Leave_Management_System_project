
from django import forms
from .models import Holiday

class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['name', 'date']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
