# in your signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, LeaveType, EmployeeLeaveBalance

@receiver(post_save, sender=Employee)
def initialize_leave_balances(sender, instance, created, **kwargs):
    if created:
        leave_types = LeaveType.objects.all()

        for leave_type in leave_types:
            EmployeeLeaveBalance.objects.create(
                employee=instance,
                leave_type=leave_type,
                balance=leave_type.leave_days
            )
