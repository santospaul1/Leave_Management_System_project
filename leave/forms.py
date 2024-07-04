from leave.models import LeaveType

from django import forms

class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['leavetype', 'Description', 'leave_days']


class LeaveForm(forms.Form):
    fromdate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    todate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    leavetype = forms.ChoiceField(choices=[('', 'Select Leave Type')], required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        leave_types = LeaveType.objects.all().values_list('leavetype', 'leavetype')
        self.fields['leavetype'] = forms.ChoiceField(choices=[('', 'Select Leave Type')] + list(leave_types), required=True)


class LeaveActionForm(forms.Form):
    action = forms.ChoiceField(
        choices=((1, 'Approve'), (2, 'Decline')),
        required=True,
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Description', 'maxlength': 500}),
        required=True,
    )

