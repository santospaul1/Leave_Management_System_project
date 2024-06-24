from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from notification.models import Notification
from .models import Employee, Leave, LeaveType, EmployeeLeaveBalance
from django.dispatch import receiver
from django.db.models.signals import post_save

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
@receiver(post_save, sender=LeaveType)

def initialize_leave_type_balances(sender, instance, created, **kwargs):
    if created:
        employees = Employee.objects.all()

        for employee in employees:
            EmployeeLeaveBalance.objects.create(
                employee=employee,
                leave_type=instance,
                balance=instance.leave_days
            )

@receiver(post_save, sender=Leave)
def send_leave_notification(sender, instance, created, **kwargs):
    if created:
        # Notify admins
        admin_users = User.objects.filter(is_staff=True)
        for admin in admin_users:
            Notification.objects.create(
                recipient=admin,
                message=f"{instance.employee.user.username} has applied for leave."
            )
    else:
        # Notify the employee
        Notification.objects.create(
            recipient=instance.employee.user,
            message=f"Your leave request has been {'approved' if instance.status == '1' else 'declined'}."
        )