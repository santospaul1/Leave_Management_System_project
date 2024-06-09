from django.shortcuts import redirect, render,get_object_or_404

from employee.models import Employee
from leave.forms import LeaveActionForm, LeaveForm, LeaveTypeForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from leave.models import EmployeeLeaveBalance, Leave, LeaveType

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

    if request.method == "POST":
        form = LeaveActionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            action = form.cleaned_data['action']
            leave.admin_remark = description
            leave.status = action  # Renamed from status to action
            leave.save()

            if action == '1':  # If the leave is approved
                leave_days = (leave.todate - leave.fromdate).days   # Calculate the number of leave days
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
def leaves_history(request):
    if not request.user.is_authenticated:
        return redirect('myadmin:admin_login')  # Redirect to the login page if not authenticated

    leave_history = Leave.objects.select_related('employee').order_by('-id')  # Assuming you have a Leave model
    return render(request, 'leaves/leaves_history.html', {'leave_history': leave_history})

@login_required
def leave_type_section(request):
    if not request.user.is_authenticated:
        return redirect('myadmin:admin_login')  # Redirect to the login page if not authenticated

    if request.method == 'GET' and 'del' in request.GET:
        leave_type_id = request.GET['del']
        try:
            leave_type = LeaveType.objects.get(id=leave_type_id)
            leave_type.delete()
            messages.success(request, 'Leave type record deleted')
        except LeaveType.DoesNotExist:
            messages.error(request, 'Leave type record not found')

    leave_types = LeaveType.objects.all()

    return render(request, 'leaves/leave_type_section.html', {'leave_types': leave_types})

@login_required
def pending_leaves(request):
    leaves = Leave.objects.filter(status=0).order_by('-id')

    context = {
        'leaves': leaves
    }
    return render(request, 'leaves/pending_history.html', context)

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
                return render(request, 'leaves/apply_leave.html', {
                    'form': form,
                    'error': 'Invalid leave type selected.'
                })

            # Get the Employee instance associated with the logged-in user
            try:
                employee = Employee.objects.get(user=request.user)
            except Employee.DoesNotExist:
                error = "Employee profile not found for the current user."
                return render(request, 'employee/apply_leave.html', {'form': form, 'error': error})
            
            days = (todate - fromdate).days + 1


            if days < 0:
                error = "End Date should be after Starting Date"
            else:
                    Leave.objects.create(
                    employee=employee,
                    leavetype=leavetype,
                    fromdate=fromdate,
                    todate=todate,
                    description=description,
                    status=0,  
                    days=days
                
                )
                    msg = "Leave application submitted successfully."
                
        else:
            error = "Form is not valid."
    else:
        form = LeaveForm()

    return render(request, 'employee/apply_leave.html', {'form': form, 'error': error, 'msg': msg})

@login_required
def employee_leave_history(request):
    user = request.user

    try:
        # Retrieve the Employee instance associated with the logged-in user
        employee = Employee.objects.get(user=user)
    except Employee.DoesNotExist:
        # Handle the case where the Employee instance does not exist
        error = "Employee profile not found for the current user."
        return render(request, 'leaves/leave_history.html', {'error': error})

    # Filter leave history by the Employee instance
    leave_history = Leave.objects.filter(employee=employee).order_by('-id')
    status = Leave.status

    context = {
        'status': status,
        'leave_history': leave_history
    }

    return render(request, 'employee/leave_history.html', context)

@login_required
def leave_balance(request): #Calculates leave balance
    employee = Employee.objects.get(user=request.user)
    leave_balances = EmployeeLeaveBalance.objects.filter(employee=employee)
    context = {
        'employee': employee,
        'leave_balances': leave_balances
    }
    return render(request, 'leaves/leave_balance.html', context)

