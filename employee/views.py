from django.shortcuts import get_object_or_404, redirect, render

from employee.forms import EmployeeForm, EmployeeUpdateForm, ProfileUpdateForm

from django.contrib.auth.models import User

from employee.models import Employee

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from leave.models import EmployeeLeaveBalance, Leave
from notification.models import Notification

@login_required
def employees(request):

    if not request.user.is_authenticated:
        return redirect('myadmin:admin_login')  # Redirect to the appropriate URL

    msg = None

    if request.method == 'GET':
        if 'inid' in request.GET:
            id = request.GET.get('inid')
            status = "Inactive"
            employee = Employee.objects.get(id=id)
            employee.Status = status
            employee.save()
            return redirect('employees')

        if 'id' in request.GET:
            id = request.GET.get('id')
            status = "Active"
            employee = Employee.objects.get(id=id)
            employee.Status = status
            employee.save()
            return redirect('employees')

    employees = Employee.objects.all()

    context = {
        'employees': employees,
        'msg': msg
    }

    return render(request, 'employee/employees.html', context)

def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            # Create a new User and Employee instance
            user = User.objects.create_user(
                username=form.cleaned_data['empcode'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['firstName'],
                last_name=form.cleaned_data['lastName'],

            )

            employee = form.save(commit=False)  # Create an Employee instance but don't save it yet
            employee.user = user  # Associate the user with the employee
            employee.save()  # Now save the employee to the database

            # Redirect to a success page or handle success as needed
            messages.success(request, 'New employee has been added successfully')
            return redirect('employee:employees')

    else:
        form = EmployeeForm()

    return render(request, 'employee/add_employee.html', {'form': form})

@login_required
def delete_employee(request):
    if request.method == "GET" and 'del' in request.GET:
        empcode = request.GET.get('del')
        try:
            employee = Employee.objects.get(empcode=empcode)
            employee.delete()
            messages.success(request, "The selected employee account has been deleted")
        except Employee.DoesNotExist:
            messages.error(request, "Employee account not found")

    employee = Employee.objects.all()
    return render(request, 'employee/employees.html', {'employee': employee})


@login_required
def update_employee(request, empcode):

  employee = get_object_or_404(Employee, empcode=empcode)

  form = EmployeeUpdateForm(instance=employee)

  if request.method == 'POST':
    form = EmployeeUpdateForm(request.POST, instance=employee)
    if form.is_valid():
      form.save()
      return redirect('employee:employees')

  return render(request, 'employee/update.html', {'form': form, 'employee': employee})

@login_required
def view_employee(request, empcode):

  employee = get_object_or_404(Employee, empcode=empcode)
  leave_history = Leave.objects.filter(employee=employee).order_by('-id')
  form = EmployeeForm(instance=employee)

  context = {
        'employee': employee,
        'leave_history': leave_history,
        'form':form,
    }
  
  return render(request, 'employee/view.html', context)

@login_required
def view_employee_leaves(request, empcode):

  employee = get_object_or_404(Employee, empcode=empcode)
  leave_history = Leave.objects.filter(employee=employee).order_by('-id')
  leave_balances = EmployeeLeaveBalance.objects.filter(employee=employee)
  

  context = {
        'employee': employee,
        'leave_history': leave_history,
        'leave_balances':leave_balances
        
    }
  
  return render(request, 'employee/view_employee_leaves.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']

        user = request.user

        if user.check_password(password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Your Password Has Been Updated.')
            else:
                messages.error(request, 'New Password and Confirm Password do not match.')
        else:
            messages.error(request, 'Your current password is wrong.')
    employee = Employee.objects.get(user=request.user)
    user_notifications = Notification.objects.filter(recipient=request.user, is_read = False).order_by('-timestamp')

    return render(request, 'employee/change_password.html', {'employee':employee, 'notifications':user_notifications})

@login_required()
def logout(request):
    # Clear session data
    request.session.flush()
    return redirect('accounts:employee_login')  # Redirect to the 'index' URL name or any other URL


@login_required
def employee_profile(request, empcode):
    employee = get_object_or_404(Employee, empcode=empcode)
    user_notifications = Notification.objects.filter(recipient=request.user, is_read = False).order_by('-timestamp')

    return render(request, 'employee/employee_details.html', {'employee': employee, 'notifications':user_notifications})

@login_required()
def update_profile(request, empcode):

  employee = get_object_or_404(Employee, empcode=empcode)

  form = ProfileUpdateForm(instance=employee)

  if request.method == 'POST':
    form = ProfileUpdateForm(request.POST,request.FILES, instance=employee)
    if form.is_valid():
      form.save()
      return redirect('leave:apply_leave')
  user_notifications = Notification.objects.filter(recipient=request.user, is_read = False).order_by('-timestamp')


  return render(request, 'employee/update_profile.html', {'form': form, 'employee': employee, 'notifications':user_notifications})



