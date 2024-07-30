from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from department.models import Department
from employee.models import Employee
from leave.models import Leave, LeaveType
from notification.models import Notification
from .models import Admin

# Create your views here.
def admin_login(request):
    error=None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                admin_user = Admin.objects.get(user=user)
                login(request, user)
                return redirect('myadmin:dashboard')
            except Admin.DoesNotExist:
                error = 'You are not authorized to access this area'
        else:
            error='Invalid username or password'
    return render(request, 'admin/admin_login.html',{'error': error})


@login_required
def user_logout(request):
    logout(request)
    return redirect('myadmin:admin_login')

@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    count_employees = Employee.objects.count()
    count_leavetype = LeaveType.objects.count()
    count_department = Department.objects.count()
    count_pending = Leave.objects.filter(status = 0).count()
    count_approved = Leave.objects.filter(status = 1).count()
    count_declined = Leave.objects.filter(status = 2).count()
    leaves = Leave.objects.order_by('-id')[:7]
    user_notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    

    
    context = {
        'page': 'dashboard',
        'count_employees': count_employees,
        'count_leavetype': count_leavetype,
        'count_department': count_department,
        'count_pending': count_pending,
        'count_approved': count_approved,
        'count_declined': count_declined,
        'leaves':leaves,
        'notifications':user_notifications,
        
    }

    return render(request, 'admin/dashboard.html', context)


@login_required
def add_admin(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        # Create a new User instance
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create a new Admin instance and associate it with the created user
        admin = Admin.objects.create(
            user=user,
            fullname=fullname,
            email=email,
            username=username
        )

        messages.success(request, 'New admin has been added successfully')
        return redirect('myadmin:manage_admin')  # Redirect to the same page to show the message

    return render(request, 'admin/add_admin.html')

@login_required
def manage_admin(request):
    if request.method == "GET" and 'del' in request.GET:
        id = request.GET.get('del')
        try:
            admin = Admin.objects.get(id=id)

            admin.delete()
            messages.success(request, "The selected admin account has been deleted")
        except Admin.DoesNotExist:
            messages.error(request, "Admin account not found")

    admins = Admin.objects.all()
    return render(request, 'admin/manage_admin.html', {'admins': admins})

