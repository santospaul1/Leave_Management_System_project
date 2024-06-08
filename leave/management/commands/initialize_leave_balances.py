
from django.core.management.base import BaseCommand
from employee.models import Employee
from leave.models import LeaveType, EmployeeLeaveBalance

class Command(BaseCommand):
    help = 'Initialize leave balances for all employees'

    def handle(self, *args, **kwargs):
        employees = Employee.objects.all()
        leave_types = LeaveType.objects.all()

        for employee in employees:
            for leave_type in leave_types:
                EmployeeLeaveBalance.objects.create(
                    employee=employee,
                    leave_type=leave_type,
                    balance=leave_type.leave_days
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized leave balances for all employees'))
