from django.contrib.auth.models import User
from django.shortcuts import redirect, render,get_object_or_404
from django.utils import timezone
from department.models import Department
from employee.models import Employee
from holiday.date_utils import calculate_business_days
from leave.forms import LeaveActionForm, LeaveForm, LeaveTypeForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from leave.models import EmployeeLeaveBalance, Leave, LeaveType
from notification.models import Notification



@login_required
def add_leave_type(request): #Function to add types of leaves 
    if request.method == 'POST':
        leavetype = request.POST['leavetype']
        description = request.POST['Description']
        leave_days = request.POST['leave_days']

        leavetype = LeaveType(leavetype=leavetype, Description=description, leave_days=leave_days)
        leavetype.save()
        messages.success(request, 'New leave has been added successfully')
        return redirect('leave:leavetype_list')

    else:
        form = LeaveTypeForm()  # Render an empty form

    return render(request, 'leaves/add_leave_type.html', {'form': form})

@login_required
def leave_type_list(request): #Function to display types of leaves available 
    leave_types = LeaveType.objects.all()  # Query all leave types
    return render(request, 'leaves/leave_type_list.html', {'leave_types': leave_types})

@login_required
def leave_type_section(request): #Function to delete selected leave type
    if not request.user.is_authenticated:
        return redirect('myadmin:admin_login')  # Redirect to the login page if not authenticated

    if request.method == 'GET' and 'del' in request.GET:
        leave_type_id = request.GET['del']
        try:
            leave_type = LeaveType.objects.get(id=leave_type_id)
            leave_type.delete()
            messages.success(request, 'Leave type record deleted')
            return redirect('leave:leave_type_list')
        except LeaveType.DoesNotExist:
            messages.error(request, 'Leave type record not found')

    leave_types = LeaveType.objects.all()

    return render(request, 'leaves/leave_type_list.html', {'leave_types': leave_types})


@login_required
def update_leave_type(request, lid):
    msg = None
    if not request.user.is_authenticated:
        return redirect('myadmin:admin_login')  # Redirect to the appropriate URL

    if request.method == 'POST':

        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            leave_type = LeaveType.objects.get(id=lid)
            leave_type.leavetype = form.cleaned_data['leavetype']
            leave_type.Description = form.cleaned_data['Description']
            leave_type.leave_days = form.cleaned_data['leave_days']


            leave_type.save()

            msg = "Leave type updated successfully"

    else:
        leave_type = LeaveType.objects.get(pk=lid)
        form = LeaveTypeForm(initial={
            'leavetype': leave_type.leavetype,
            'Description': leave_type.Description,
            'leave_days': leave_type.leave_days
        })

    context = {
        'form': form,
        'msg': msg
    }

    return render(request, 'leaves/update_leave_type.html', context)


@login_required
def apply_leave(request):
    error = None
    msg = None
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            fromdate = form.cleaned_data['fromdate']
            todate = form.cleaned_data['todate']
            leavetype_str = form.cleaned_data['leavetype']
            description = form.cleaned_data['description']

            try:
                leavetype = LeaveType.objects.get(leavetype=leavetype_str)
            except LeaveType.DoesNotExist:
                return render(request, 'employee/apply_leave.html', {
                    'form': form,
                    'error': 'Invalid leave type selected.'
                })

            # Get the Employee instance associated with the logged-in user
            try:
                employee = Employee.objects.get(user=request.user)
            except Employee.DoesNotExist:
                error = "Employee profile not found for the current user."
                return render(request, 'employee/apply_leave.html', {'form': form, 'error': error})
            
            # Check leave balance for the specified leave type
            try:
                leave_balance = EmployeeLeaveBalance.objects.get(employee=employee, leave_type=leavetype)
            except EmployeeLeaveBalance.DoesNotExist:
                error = "Leave balance not found for the specified leave type."
                return render(request, 'employee/apply_leave.html', {'form': form, 'error': error})

            business_days = calculate_business_days(fromdate, todate)
            current_date = timezone.now().date()

            if business_days <= 0:
                error = "End Date should be after Starting Date."
            elif fromdate < current_date or todate < current_date:
                error = "Please correct the date and retry."
            elif business_days > leave_balance.balance:
                error = f"You do not have enough leave days. You have {leave_balance.balance} days available."
            else:
                Leave.objects.create(
                    employee=employee,
                    leavetype=leavetype,
                    fromdate=fromdate,
                    todate=todate,
                    description=description,
                    status=0,  # Pending status
                    days=business_days
                )
                msg = "Leave application submitted successfully."
                
                
        else:
            error = "Form is not valid."
    else:
        form = LeaveForm()
    employee = Employee.objects.get(user=request.user)
    user_notifications = Notification.objects.filter(recipient=request.user, is_read = False).order_by('-timestamp')
    
    return render(request, 'employee/apply_leave.html', {'form': form, 'employee': employee, 'error': error, 'msg': msg,'notifications':user_notifications})



@login_required
def employee_leave_history(request):
    user = request.user

    try:
        # Retrieve the Employee instance associated with the logged-in user
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        # Handle the case where the Employee instance does not exist
        error = "Employee profile not found for the current user."
        return render(request, 'employee/leave_history.html', {'error': error})

    # Filter leave history by the Employee instance
    leave_history = Leave.objects.filter(employee=employee).order_by('-id')
    status = Leave.status
    user_notifications = Notification.objects.filter(recipient=request.user, is_read = False).order_by('-timestamp')

    context = {
        'status': status,
        'leave_history': leave_history,
        'employee':employee,
        'notifications':user_notifications
    }

    return render(request, 'employee/leave_history.html', context)

@login_required
def leave_balance(request): #Calculates leave balance
    employee = Employee.objects.get(user=request.user)
    leave_balances = EmployeeLeaveBalance.objects.filter(employee=employee)
    user_notifications = Notification.objects.filter(recipient=request.user, is_read = False).order_by('-timestamp')

    context = {
        'employee': employee,
        'leave_balances': leave_balances,
        'notifications':user_notifications
    }
    return render(request, 'leaves/leave_balance.html', context)



@login_required
def approved_leaves(request):
    
    approved_leaves = Leave.objects.filter(status=1)
    context = {
        
        'approved_leaves': approved_leaves,
    }
    
    return render(request, 'leaves/approved_leaves.html', context)

@login_required
def employee_leave_details(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    error = ''
    msg = ''
    message  = None

    if request.method == "POST":
        form = LeaveActionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            action = form.cleaned_data['action']
            leave.admin_remark = description
            leave.status = action  # Renamed from status to action
            leave.save()

            if action == '1':  # If the leave is approved
                leave_days = calculate_business_days(leave.fromdate, leave.todate)   # Calculate the number of leave days
                employee = leave.employee

                try:
                    leave_type_instance = LeaveType.objects.get(leavetype=leave.leavetype)
                    leave_balance = EmployeeLeaveBalance.objects.get(employee=employee, leave_type=leave_type_instance)
                except (LeaveType.DoesNotExist, EmployeeLeaveBalance.DoesNotExist):
                    error = f"Leave balance for {employee.user.username} and {leave.leavetype} not found."
                else:
                    if leave_balance.balance >= leave_days:
                        leave_balance.balance -= leave_days
                        leave_balance.save()
                        msg = f"Leave balance updated for {employee.user.username}."
                    else:
                        error = f"Not enough leave days available for {employee.user.username}."
                        leave.status = '0'  # Revert to pending if not enough leave days
                        leave.save()
            else:
                msg = "Leave declined successfully."

            if error:
                messages.error(request, error)
            else:
                messages.success(request, msg)
            
        else:
            error = "Please correct the form errors."
            messages.error(request, error)
    else:
        form = LeaveActionForm(initial={'action': leave.status})
    
    context = {
        'form': form,
        'leave': leave,
        'error': error,
        'msg': msg,  
    }

    return render(request, 'leaves/leave_details.html', context)
@login_required
def declined_leaves(request):
    declined_leaves = Leave.objects.filter(status=2).order_by('-id')
    context = {
        'declined_leaves': declined_leaves
    }
    return render(request, 'leaves/declined_leaves.html', context)


@login_required
def leaves_history(request):
    if not request.user.is_authenticated:
        return redirect('myadmin:admin_login')  # Redirect to the login page if not authenticated

    leave_history = Leave.objects.select_related('employee').order_by('-id')  # Assuming you have a Leave model
    return render(request, 'leaves/leaves_history.html', {'leave_history': leave_history})



@login_required
def pending_leaves(request):
    leaves = Leave.objects.filter(status=0).order_by('-id')

    context = {
        'leaves': leaves
    }
    return render(request, 'leaves/pending_history.html', context)


@login_required
def employees_on_leave_per_department(request):
    current_date = timezone.now().date()
    
    # Filter leaves where the current date is between the start and end date
    current_leaves = Leave.objects.filter(fromdate__lte=current_date, todate__gte=current_date, status=1)
    
    # Group leaves by department
    departments = Department.objects.all()
    department_leave_data = {}

    for department in departments:
        employees_on_leave = Employee.objects.filter(department=department, leave__in=current_leaves)
        if employees_on_leave.exists():
            department_leave_data[department] = {}
            for employee in employees_on_leave:
                current_leave = current_leaves.filter(employee=employee).first()
                if current_leave:
                    department_leave_data[department][employee] = current_leave

    return render(request, 'leaves/department_leave.html', {'department_leave_data': department_leave_data})

@login_required
def employees_going_on_leave_per_department(request):
    current_date = timezone.now().date()
    
    # Filter upcoming leaves
    upcoming_leaves = Leave.objects.filter(fromdate__gt=current_date, status=1).order_by('fromdate')
    
    # Group leaves by department
    departments = Department.objects.all()
    department_leave_data = {}

    for department in departments:
        department_leaves = upcoming_leaves.filter(employee__department=department)
        if department_leaves.exists():
            department_leave_data[department] = department_leaves

    return render(request, 'leaves/upcoming_leaves.html', {'department_leave_data': department_leave_data})

