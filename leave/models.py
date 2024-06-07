from django.db import models
from employee.models import Employee

# Create your models here.

STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Approved'),
        (2, 'Declined')
    )
class LeaveType(models.Model):
    leavetype = models.CharField(max_length=255)
    Description = models.TextField()
    leave_days = models.IntegerField(default = 30)
    PostingDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.leavetype


class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    posting_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    leavetype = models.CharField(max_length=255, default=None)
    description = models.TextField(default=None)
    fromdate = models.DateField( default=None)
    todate = models.DateField( default=None)
    days = models.IntegerField(default=0)
    isread = models.IntegerField(default=0)
    admin_remark = models.CharField(max_length=255, default=None, null=True)

