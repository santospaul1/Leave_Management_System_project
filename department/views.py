from django.shortcuts import redirect, render

from django.db.models import Q

from department.models import Department

from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Create your views here.
@login_required
def department(request):
    if request.method == "GET" and 'del' in request.GET:
        department_id = request.GET['del']
        try:
            department = Department.objects.get(id=department_id)
            department.delete()
            messages.success(request, "Department deleted successfully")
        except Department.DoesNotExist:
            messages.error(request, "Department not found")

    departments = Department.objects.all()
    return render(request, 'department/department_list.html', {'departments': departments})

@login_required
def add_department(request):
    if request.method == 'POST':
        department_name = request.POST.get('department_name')
        department_shortname = request.POST.get('department_shortname')
        department_code = request.POST.get('department_code')

        department = Department(department_name=department_name, department_shortname=department_shortname,
                                department_code=department_code)
        Department.objects.filter(Q(department_name__isnull=True) | Q(department_shortname__isnull=True)).delete()
        department.save()

        messages.success(request, 'New department has been added successfully')
        return redirect('department:department')

    return render(request, 'department/add_department.html')

@login_required
def update_department(request, deptid):
    global department
    if not request.session.get('alogin'):
        return redirect('myadmin:admin_login')  # Redirect to the login page if not logged in

    error = None
    msg = None

    if request.method == 'POST':
        deptname = request.POST.get('departmentname')
        deptshortname = request.POST.get('departmentshortname')
        deptcode = request.POST.get('deptcode')

        try:
            department = Department.objects.get(id=deptid)
            department.DepartmentName = deptname
            department.DepartmentShortName = deptshortname
            department.DepartmentCode = deptcode
            department.save()
            msg = "Department updated successfully"
        except Department.DoesNotExist:
            error = "Department not found or already deleted"

    try:
        department = Department.objects.get(id=deptid)
    except Department.DoesNotExist:
        error = "Department not found"

    context = {
        'error': error,
        'msg': msg,
        'department': department,
    }

    return render(request, 'department/update_department.html', context)

