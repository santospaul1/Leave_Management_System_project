from django.shortcuts import redirect, render

from employee.models import Employee
from leave.forms import LeaveActionForm, LeaveForm, LeaveTypeForm

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from leave.models import Leave, LeaveType

@login_required
def add_leave_type(request):
    if request.method == 'POST':
        leavetype = request.POST['leavetype']
        description = request.POST['Description']

        leavetype = LeaveType(leavetype=leavetype, Description=description)
        leavetype.save()

        # Redirect to a success page or handle success as needed
        messages.success(request, 'New leave has been added successfully')
        return redirect('leave:leavetype_list')

    else:
        form = LeaveTypeForm()  # Render an empty form

    return render(request, 'leaves/add_leave_type.html', {'form': form})

@login_required
def leave_type_list(request):
    leave_types = LeaveType.objects.all()  # Query all leave types
    return render(request, 'leaves/leave_type_list.html', {'leave_types': leave_types})

@login_required
def approved_leaves(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to your login page
    error = None
    msg = None
    approved_leaves = Leave.objects.filter(status=1)

    if request.method == 'POST':
        query = Leave.objects.all()

        # Execute the query and get the results
        results = query.values()

        # Get the count of results
        leavtypcount = query.count()
    leaves = Leave.objects.filter(status=1).order_by('-id')

    context = {
        'error': error,
        'msg': msg,
        'approved_leaves': approved_leaves,
    }
    return render(request, 'leaves/approved_leaves.html', context)

@login_required
def employee_leave_details(request, leave_id):
    if not request.user.is_authenticated:
        return redirect('leave:admin_login')  # Redirect to the login page if the user is not authenticated

    error = ''
    msg = ''
    leave = Leave.objects.get(pk=leave_id)

    if request.method == "POST":
        form = LeaveActionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            action = form.cleaned_data['action']
            leave.admin_remark = description
            leave.status = action  # Renamed from status to action
            leave.save()
            msg = "Leave updated Successfully"
        else:
            error = "Please correct the form errors."
    else:
        form = LeaveActionForm(initial={'action': leave.status})  # Renamed from status to action

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
    global msg
    if not request.user.is_authenticated:
        return redirect('myadmin:admin_login')  # Redirect to the appropriate URL

    if request.method == 'POST':

        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            leave_type = LeaveType.objects.get(id=lid)
            leave_type.leavetype = form.cleaned_data['leavetype']
            leave_type.Description = form.cleaned_data['Description']
            leave_type.save()

            msg = "Leave type updated successfully"

    else:
        leave_type = LeaveType.objects.get(pk=lid)
        form = LeaveTypeForm(initial={
            'leavetype': leave_type.leavetype,
            'Description': leave_type.Description
        })

    context = {
        'form': form,
        'msg': msg if 'msg' in locals() else None
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
            leavetype = form.cleaned_data['leavetype']
            description = form.cleaned_data['description']

            # Get the Employee instance associated with the logged-in user
            try:
                employee = Employee.objects.get(user=request.user)
            except Employee.DoesNotExist:
                error = "Employee profile not found for the current user."
                return render(request, 'employee/apply_leave.html', {'form': form, 'error': error})

            try:
                Leave.objects.create(
                    employee=employee,
                    leavetype=leavetype,
                    fromdate=fromdate,
                    todate=todate,
                    description=description,
                    status=0  # Assuming 0 is the status for 'Pending'
                )
                msg = "Leave application submitted successfully."


            except Exception as e:
                error = str(e)
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



